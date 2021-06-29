from application import models
from application import serializers
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from rest_framework.decorators import api_view
from rest_framework.parsers import MultiPartParser
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound, HttpResponseForbidden, HttpResponseBadRequest
from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import logging
import os
from sendfile import sendfile
from sticky_link.settings import MEDIA_BASE_PATH
from itertools import chain

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
    def port(request, pk):
        # Resolve redirection to required resource
        user = request.user
        try:
            port = models.Port.get_anonymous_ports(user).get(pk=pk)
        except models.Port.DoesNotExist:
            return HttpResponseNotFound('Port does not exist')

        port.visited += 1  # Update port statistics
        port.save()

        wall = port.resolve_target_wall(user)
        if wall is None:
            if port.redirect_url is not None:
                return redirect(port.redirect_url)
            return HttpResponseNotFound('Invalid resource')

        return redirect(f'/wall/view/{wall.id}/')

    @classmethod
    def _retrieve_state(cls, request, pk):
        user = request.user
        containers = []
        widgets = []
        try:
            wall = models.Wall.get_reachable(user).get(pk=pk)
        except models.Wall.DoesNotExist:
            return abort('Wall is unreachable', 404)
        wall.set_permission(user)
        for container in wall.container_set.all():
            for w in container.simple_text_set.all():
                widgets.append(serializers.SimpleTextSerializer(w).data)

            for w in container.url_set.all():
                widgets.append(serializers.URLSerializer(w).data)

            for w in container.simple_list_set.all():
                widgets.append(serializers.SimpleListSerializer(w).data)

            for w in container.counter_set.all():
                widgets.append(serializers.CounterSerializer(w).data)

            for w in container.simple_switch_set.all():
                widgets.append(serializers.SimpleSwitchSerializer(w).data)

            for w in container.document_set.all():
                widgets.append(serializers.DocumentSerializer(w).data)
            containers.append(serializers.ContainerSerializer(container).data)
        if not containers:
            containers = [serializers.ContainerSerializer(wall.initiate_default_container()).data]

        meta = serializers.Meta(models.Meta()).data
        wall = serializers.WallSerializer(wall).data
        walls = [wall]

        ports = serializers.PortSerializer(models.Port.get_owned_ports(user), many=True).data
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
        ports = serializers.PortSerializer(models.Port.get_owned_ports(user), many=True).data
        walls = []
        for wall in chain(models.Wall.get_owned_walls(user), models.Wall.get_trusted_walls(user)):
            wall.set_permission(user)
            wall = serializers.WallSerializer(wall).data
            walls.append(wall)
        containers = []
        widgets = []
        meta = serializers.Meta(models.Meta()).data

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
                return models.User.objects.get(username=username)
            except models.User.DoesNotExist:
                return None

        def get_wall():
            try:
                # Only trusted user (owner is trusted) may add trusted users!
                return models.Wall.get_owned_walls(request.user).get(pk=pk)
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


class ProtectedModelViewSet(ModelViewSet):
    model_class = None
    anonymous_actions = ['list', 'retrieve', 'partial_update', 'update']

    def update(self, request, *args, **kwargs):
        user = request.user
        instance = self.model_class.objects.get(pk=self.kwargs['pk'])
        if not instance.has_anonymous_permission(user) and \
                not instance.has_trusted_permission(user) and \
                not instance.has_owner_permission(user):
            return abort('Forbidden', 403)
        if user.is_anonymous and not instance.validate_anonymous_access(request.data.keys()):
            return abort('Forbidden', 403)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        user = request.user
        instance = self.model_class.objects.get(pk=self.kwargs['pk'])
        if not instance.has_trusted_permission(user) and not instance.has_owner_permission(user):
            return abort('Forbidden', 403)
        return super().destroy(request, *args, **kwargs)

    def get_permissions(self):
        return [] if self.action in self.anonymous_actions else [IsAuthenticated()]

    def get_queryset(self):
        return self.model_class.get_reachable(self.request.user)

    def get_object(self):
        obj = super().get_object()
        obj.set_permission()
        return obj


class WallViewSet(ProtectedModelViewSet):
    serializer_class = serializers.WallSerializer
    model_class = models.Wall

    def update(self, request, *args, **kwargs):
        user = request.user
        wall = self.model_class.objects.get(pk=self.kwargs['pk'])
        if not wall.has_owner_permission(user):
            return abort('Forbidden', 403)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        user = request.user
        wall = self.model_class.objects.get(pk=self.kwargs['pk'])
        if not wall.has_owner_permission(user):
            return abort('Forbidden', 403)
        return super().destroy(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        return JsonResponse([
            *serializers.WallSerializer(self.model_class.get_owned_walls(request.user), many=True).data,
            *serializers.WallSerializer(self.model_class.get_trusted_walls(request.user), many=True).data
        ], safe=False)

    def create(self, request, *args, **kwargs):
        request.data['owner'] = request.user.id  # Trust only inside user id
        return super().create(request, *args, **kwargs)


class ContainerViewSet(ProtectedModelViewSet):
    serializer_class = serializers.ContainerSerializer
    model_class = models.Container


class PortViewSet(ProtectedModelViewSet):
    serializer_class = serializers.PortSerializer
    model_class = models.Port

    def get_queryset(self):
        return self.model_class.get_owned_ports(self.request.user)

    def create(self, request, *args, **kwargs):
        request.data['owner'] = request.user.id  # Trust only inside user id
        return super().create(request, *args, **kwargs)


class SourceViewSet(ProtectedModelViewSet):
    parser_classes = [MultiPartParser]
    model_class = models.Source
    serializer_class = serializers.SourceSerializer

    def get_object(self):
        return self.get_queryset().filter(id=self.kwargs['pk']).first()

    def create(self, request, *args, **kwargs):
        return HttpResponseForbidden()  # Sources will be managed manually

    def list(self, request, *args, **kwargs):
        return HttpResponseForbidden()

    def retrieve(self, request, *args, **kwargs):
        # Return file that is stored by source
        try:
            source = self.get_object()
        except self.model_class.DoesNotExist:
            return abort('Not found', 404)
        if source.file is None:
            return abort('Not found', 404)
        return sendfile(request, MEDIA_BASE_PATH + '/' + source.file.name, attachment=request.GET.get('attachment'))

    def update(self, request, *args, **kwargs):
        user = request.user
        # Replace stored file
        try:
            source = self.get_object()
        except self.model_class.DoesNotExist:
            return abort('Not found', 404)
        if not source.has_trusted_permission(user) and not source.has_owner_permission(user):
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

        for parent in source.parent.all():
            parent.propagate_instance_updated()
        return response

    def destroy(self, request, *args, **kwargs):
        # Delete file, not source object. Source will be deleted simultaneously with parent
        user = request.user
        source = self.model_class.objects.get(pk=self.kwargs['pk'])
        if not source.has_trusted_permission(user) and not source.has_owner_permission(user):
            return abort('Forbidden', 403)
        try:
            source = self.get_object()
        except self.model_class.DoesNotExist:
            return abort('Not found', 404)
        source.delete_file()
        for parent in source.parent.all():
            parent.propagate_instance_updated()
        return Response('Ok')


class SyncViewSet(ProtectedModelViewSet):

    def update(self, request, pk=None, *args, **kwargs):
        if not self.model_class.has_any_sync_widget(request.user, request.data.get('sync_id')):
            return JsonResponse({
                'sync_id': ['Make sure the sync ID belong to user and widgets have the same type.']
            }, status=400)
        return super().update(request, *args, **kwargs)


class SimpleTextViewSet(SyncViewSet):
    serializer_class = serializers.SimpleTextSerializer
    model_class = models.SimpleText


class URLViewSet(SyncViewSet):
    serializer_class = serializers.URLSerializer
    model_class = models.URL


class SimpleListViewSet(SyncViewSet):
    serializer_class = serializers.SimpleListSerializer
    model_class = models.SimpleList


class CounterViewSet(SyncViewSet):
    serializer_class = serializers.CounterSerializer
    model_class = models.Counter


class SimpleSwitchViewSet(SyncViewSet):
    serializer_class = serializers.SimpleSwitchSerializer
    model_class = models.SimpleSwitch


class DocumentViewSet(SyncViewSet):
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
        return response
