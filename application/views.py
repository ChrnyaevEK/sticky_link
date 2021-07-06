import os
import logging
from itertools import chain
from sendfile import sendfile

from application import models
from application import serializers
from sticky_link.settings import MEDIA_BASE_PATH

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.http import JsonResponse, HttpResponse, HttpResponseNotFound, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)


def abort(msg, status=400):
    return JsonResponse({
        'detail': msg
    }, status=status)


class App:
    @staticmethod
    @api_view(http_method_names=['GET'])
    def enter(request):
        # Entry point for users - resolve on enter redirections, return client app
        template = 'application/dist/index.html'
        return HttpResponse(render(request, template))

    @staticmethod
    @api_view(http_method_names=['GET', 'POST'])
    def port(request, pk):
        # Resolve redirection to required resource
        user = request.user
        try:
            port = models.Port.get_anonymous(user).get(pk=pk)
        except models.Port.DoesNotExist:
            return HttpResponseNotFound('Port does not exist')
        if request.method == 'GET':
            if not port.activated:
                return redirect(f'/port/activation/{port.id}')

            port.visited += 1
            port.save()

            wall = port.resolve_target_wall(user)
            if wall is None:
                if port.redirect_url is not None:
                    return redirect(port.redirect_url)
                return HttpResponseNotFound('Invalid resource')

            return redirect(f'/wall/view/{wall.id}')
        else:
            if user.is_authenticated:
                if not port.activated:
                    port.activate(user)
                    port.save()
                    return JsonResponse(serializers.PortSerializer(port).data)
                else:
                    return abort('Forbidden', 403)
            else:
                return abort('Not authenticated', 403)

    @classmethod
    def _retrieve_state(cls, request, pk):
        user = request.user
        containers = []
        widgets = []
        try:
            wall = models.Wall.get_reachable(user).get(pk=pk)
        except models.Wall.DoesNotExist:
            return abort('Wall is unreachable', 403)
        wall.set_permission(user)
        for container in wall.container_set.all():
            for w in container.simpletext_set.all():
                widgets.append(serializers.SimpleTextSerializer(w).data)

            for w in container.url_set.all():
                widgets.append(serializers.URLSerializer(w).data)

            for w in container.simplelist_set.all():
                widgets.append(serializers.SimpleListSerializer(w).data)

            for w in container.counter_set.all():
                widgets.append(serializers.CounterSerializer(w).data)

            for w in container.simpleswitch_set.all():
                widgets.append(serializers.SimpleSwitchSerializer(w).data)

            for w in container.document_set.all():
                widgets.append(serializers.DocumentSerializer(w).data)
            containers.append(serializers.ContainerSerializer(container).data)
        if not containers:
            containers = [serializers.ContainerSerializer(wall.initiate_default_container()).data]

        meta = serializers.Meta(models.Meta()).data
        wall = serializers.WallSerializer(wall).data
        walls = [wall]

        ports = serializers.PortSerializer(models.Port.get_owned(user), many=True).data
        return JsonResponse({
            'user': serializers.UserSerializer(user).data,
            'containers': containers,
            'ports': ports,
            'widgets': widgets,
            'walls': walls,
            'meta': meta,
            'reference': wall,
        })

    @classmethod
    def _list_state(cls, request):
        user = request.user
        meta = serializers.Meta(models.Meta()).data
        ports = serializers.PortSerializer(models.Port.get_owned(user), many=True).data
        walls = []
        containers = []
        widgets = []

        for wall in chain(models.Wall.get_owned(user), models.Wall.get_trusted(user)):
            wall.set_permission(user)
            wall = serializers.WallSerializer(wall).data
            walls.append(wall)

        return JsonResponse({
            'user': serializers.UserSerializer(user).data,
            'containers': containers,
            'ports': ports,
            'widgets': widgets,
            'walls': walls,
            'meta': meta,
            'reference': None
        })

    @staticmethod
    @api_view(http_method_names=['GET'])
    def state(request, pk=None):
        if pk is None:
            return App._list_state(request)
        else:
            return App._retrieve_state(request, pk)

    @staticmethod
    @api_view(http_method_names=['GET', 'POST', 'DELETE'])
    def trusted_user(request):
        username = request.GET.get('username')
        pk = request.GET.get('wall')

        def get_user():
            try:
                return User.objects.get(username=username)
            except User.DoesNotExist:
                return None

        def get_wall():
            try:
                # Only trusted user (owner is trusted) may add trusted users!
                return models.Wall.get_owned(request.user).get(pk=pk)
            except models.Wall.DoesNotExist:
                return None

        if request.method == 'GET':
            user = get_user()
            if user is None:
                return JsonResponse(None, safe=False)
            else:
                return JsonResponse(serializers.UserSerializer(user).data)
        elif request.method == 'POST':
            user = get_user()
            if user is None:
                return abort('Forbidden', 403)
            wall = get_wall()
            if wall is None:
                return abort('Forbidden', 403)
            if wall.owner != user:
                wall.trusted_users.add(user)
                wall.save()
            return JsonResponse(serializers.WallSerializer(wall).data)
        elif request.method == 'DELETE':
            user = get_user()
            if user is None:
                return abort('Forbidden', 403)
            wall = get_wall()
            if wall is None:
                return abort('Forbidden', 403)
            wall.trusted_users.remove(user)
            wall.save()
            return JsonResponse(serializers.WallSerializer(wall).data)

    @staticmethod
    @api_view(http_method_names=['POST'])
    def copy_wall(request, pk):
        user = request.user
        try:
            wall = models.Wall.get_owned(user).get(pk=pk)
        except models.Wall.DoesNotExist:
            return abort('Wall is unreachable', 403)
        clone = wall.copy()
        clone.set_permission(user)
        return JsonResponse(serializers.WallSerializer(clone).data)

    @staticmethod
    @api_view(http_method_names=['POST'])
    def copy_container(request, pk):
        user = request.user
        try:
            container = models.Container.get_reachable(user).get(pk=pk)
        except models.Container.DoesNotExist:
            return abort('Container is unreachable', 403)
        clone = container.copy()
        clone.set_permission(user)
        return JsonResponse(serializers.ContainerSerializer(clone).data)


class AnonymousModelViewSet(ModelViewSet):
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.anonymous_permission and not instance.trusted_permission and not instance.owner_permission:
            return abort('Forbidden', 403)
        if request.user.is_anonymous and not instance.validate_anonymous_access(request.data.keys()):
            return abort('Forbidden', 403)
        try:
            if not self.model_class.exists(request.data['sync_id']):
                return JsonResponse({
                    'sync_id': ['Make sure the sync ID belong to user and widgets have the same type.']
                }, status=400)
        except KeyError:
            pass
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.trusted_permission and not instance.owner_permission:
            return abort('Forbidden', 403)
        return super().destroy(request, *args, **kwargs)

    def get_permissions(self):
        return [] if self.action in ['list', 'retrieve', 'partial_update', 'update'] else [IsAuthenticated()]

    def get_queryset(self):
        return self.model_class.get_reachable(self.request.user)

    def get_object(self):
        obj = super().get_object()
        obj.set_permission(self.request.user)
        return obj


class TrustedModelViewSet(AnonymousModelViewSet):
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.owner_permission and not instance.trusted_permission:
            return abort('Forbidden', 403)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.owner_permission and not instance.trusted_permission:
            return abort('Forbidden', 403)
        return super().destroy(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        return JsonResponse([
            *self.serializer_class(self.model_class.get_owned(request.user), many=True).data,
            *self.serializer_class(self.model_class.get_trusted(request.user), many=True).data
        ], safe=False)


class OwnedModelViewSet(TrustedModelViewSet):

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.owner_permission:
            return abort('Forbidden', 403)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.owner_permission:
            return abort('Forbidden', 403)
        return super().destroy(request, *args, **kwargs)


class WallViewSet(OwnedModelViewSet):
    serializer_class = serializers.WallSerializer
    model_class = models.Wall

    def update(self, request, *args, **kwargs):
        try:
            del request.data['owner']
        except KeyError:
            pass
        return super().update(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        request.data['owner'] = request.user.id  # Trust only inside user id
        return super().create(request, *args, **kwargs)


class ContainerViewSet(TrustedModelViewSet):
    serializer_class = serializers.ContainerSerializer
    model_class = models.Container

    def update(self, request, *args, **kwargs):
        try:
            del request.data['wall']
        except KeyError:
            pass
        return super().update(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        try:
            if not models.Wall.get_editable(request.user).filter(pk=request.data['wall']).exists():
                return abort('Forbidden', 403)
        except KeyError:
            pass  # Wil be processed later at model creation
        return super().create(request, *args, **kwargs)


class PortViewSet(OwnedModelViewSet):
    serializer_class = serializers.PortSerializer
    model_class = models.Port

    def update(self, request, *args, **kwargs):
        try:
            del request.data['owner']
        except KeyError:
            pass
        return super().update(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        request.data['owner'] = request.user.id  # Trust only inside user id
        return super().create(request, *args, **kwargs)


class SourceViewSet(AnonymousModelViewSet):
    parser_classes = [MultiPartParser]
    model_class = models.Source
    serializer_class = serializers.SourceSerializer

    def create(self, request, *args, **kwargs):
        return HttpResponseForbidden()  # Sources will be managed manually

    def list(self, request, *args, **kwargs):
        return HttpResponseForbidden()

    def retrieve(self, request, *args, **kwargs):
        source = self.get_object()
        if source.file is None:
            return HttpResponseNotFound('Source was not found')
        return sendfile(request, MEDIA_BASE_PATH + '/' + source.file.name, attachment=request.GET.get('attachment'))

    def update(self, request, *args, **kwargs):
        source = self.get_object()
        if not source.trusted_permission and not source.owner_permission:
            return abort('Forbidden', 403)

        try:  # Get path before update - if update fail, do not delete file
            old_path = source.file.path
        except ValueError:
            old_path = None

        response = super().update(request, *args, **kwargs)

        try:  # Remove file after update
            os.remove(old_path)
        except (TypeError, OSError):
            pass
        for document in source.document_set.all():  # Do not move to routine (propagate only when document is updated)
            document.propagate_instance_updated()
        return response

    def destroy(self, request, *args, **kwargs):
        # Delete file, not source object. Source will be deleted simultaneously with document_set
        source = self.get_object()
        if not source.trusted_permission and not source.owner_permission:
            return abort('Forbidden', 403)
        source = self.get_object()
        source.delete_file()
        for document in source.document_set.all():  # Do not move to routine (propagate only when document is updated)
            document.propagate_instance_updated()
        return Response('Ok')


class SimpleTextViewSet(AnonymousModelViewSet):
    serializer_class = serializers.SimpleTextSerializer
    model_class = models.SimpleText


class URLViewSet(AnonymousModelViewSet):
    serializer_class = serializers.URLSerializer
    model_class = models.URL


class SimpleListViewSet(AnonymousModelViewSet):
    serializer_class = serializers.SimpleListSerializer
    model_class = models.SimpleList


class CounterViewSet(AnonymousModelViewSet):
    serializer_class = serializers.CounterSerializer
    model_class = models.Counter


class SimpleSwitchViewSet(AnonymousModelViewSet):
    serializer_class = serializers.SimpleSwitchSerializer
    model_class = models.SimpleSwitch


class DocumentViewSet(AnonymousModelViewSet):
    serializer_class = serializers.DocumentSerializer
    model_class = models.Document

    def create(self, request, *args, **kwargs):
        try:  # Handle copy widget feature
            del request.data['source']
        except KeyError:
            pass
        response = super().create(request, *args, **kwargs)

        # Add source object to store files
        document = self.get_queryset().get(id=response.data['id'])
        source = models.Source()
        source.save()
        document.source = source
        document.save()
        return JsonResponse(serializers.DocumentSerializer(document).data)
