from application import models
from application import serializers
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet, ViewSet

from rest_framework.decorators import api_view
from rest_framework.parsers import FileUploadParser, MultiPartParser
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound, HttpResponseForbidden
from django.shortcuts import render, redirect
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from application.lang import Public
import logging
import os
from sendfile import sendfile
from sticky_link.settings import MEDIA_BASE_PATH

logger = logging.getLogger(__name__)


def _get_protected_queryset(model, user):
    if model == models.Wall:
        q = Q(allow_anonymous_view=True)
        if not user.is_anonymous:
            q.add(Q(owner=user), Q.OR)
    elif model == models.Container:
        q = Q(wall__allow_anonymous_view=True)
        if not user.is_anonymous:
            q.add(Q(wall__owner=user), Q.OR)
    elif model == models.Port:
        q = Q()
        if not user.is_anonymous:
            q = Q(owner=user)
    elif model == models.Source:
        q = Q(parent__container__wall__allow_anonymous_view=True)
        if not user.is_anonymous:
            q.add(Q(parent__container__wall__owner=user), Q.OR)
    else:
        q = Q(container__wall__allow_anonymous_view=True)
        if not user.is_anonymous:
            q.add(Q(container__wall__owner=user), Q.OR)
    return model.objects.filter(q)


class App:
    @staticmethod
    @api_view(http_method_names=['GET'])
    def enter(request):
        # Entry point for users - resolve on enter redirections, return client app
        template = 'application/dist/index.html'
        return HttpResponse(render(request, template))

    @staticmethod
    def port(request, uid):
        """ Resolve redirection to required resource """
        try:
            port = models.Port.objects.get(pk=uid)
        except models.Port.DoesNotExist:
            return HttpResponseNotFound(Public.Error.port_does_not_exist)

        port.visited += 1  # Update port statistics
        port.save()

        wall = port.authenticated_wall if request.user.is_authenticated else port.anonymous_wall
        if wall is None:
            if port.redirect_url is not None:
                return redirect(port.redirect_url)
            return HttpResponseNotFound(Public.Error.port_refer_invalid_resource)

        return redirect(f'/wall/view/{wall.id}/')

    @staticmethod
    @api_view(http_method_names=['GET'])
    def state(request, wall_id=None):
        try:
            wall = _get_protected_queryset(models.Wall, request.user).get(pk=wall_id)
        except models.Wall.DoesNotExist:
            wall = None
            meta = None

            containers = []
            widgets = []
            ports = []
        else:
            containers = []
            widgets = []
            for container in _get_protected_queryset(models.Container, request.user).filter(wall=wall):
                for model, serializer in (
                        (models.SimpleText, serializers.SimpleTextSerializer),
                        (models.URL, serializers.URLSerializer),
                        (models.SimpleList, serializers.SimpleListSerializer),
                        (models.Counter, serializers.CounterSerializer),
                        (models.SimpleSwitch, serializers.SimpleSwitchSerializer),
                        (models.Document, serializers.DocumentSerializer),
                ):
                    for widget in model.objects.filter(container=container):
                        widgets.append(serializer(widget).data)
                containers.append(serializers.ContainerSerializer(container).data)
            if not containers:
                container = models.Container(wall=wall, index=0)
                container.save()
                containers = [serializers.ContainerSerializer(container).data]
            meta = {
                'edit_permission': wall.owner == request.user,
                'view_permission': wall.allow_anonymous_view or wall.owner == request.user,
                'file_size_max': 10485760,
            }
            ports = _get_protected_queryset(models.Port, request.user)
            ports = serializers.PortSerializer(ports, many=True).data
            wall = serializers.WallSerializer(wall).data
        walls = WallViewSet.generate_list(request)
        if not walls and wall:
            walls = [wall]
        elif not walls:
            walls = []

        user = serializers.UserSerializer(request.user).data
        if request.user.is_anonymous:
            user['username'] = 'anonymous'
        return JsonResponse({
            'user': user,
            'meta': meta,
            'containers': containers,
            'ports': ports,
            'widgets': widgets,
            'walls': walls
        })


class UserViewSet(ReadOnlyModelViewSet):
    serializer_class = serializers.UserSerializer

    def retrieve(self, request, *args, **kwargs):
        return JsonResponse(self.generate_user(request))

    def list(self, request, *args, **kwargs):
        return JsonResponse(self.generate_user(request))

    @staticmethod
    def generate_user(request):
        return serializers.UserSerializer(request.user).data


class CommonModelViewSet(ModelViewSet):
    model_class = None

    def get_permissions(self):
        if self.action in ('list', 'retrieve', 'partial_update', 'update'):  # Anonymous user may change data
            return []
        else:
            return [IsAuthenticated()]

    def get_queryset(self):
        return self.generate_query_set(self.request)

    @classmethod
    def generate_query_set(cls, request):
        return _get_protected_queryset(cls.model_class, request.user)


class WallViewSet(CommonModelViewSet):
    serializer_class = serializers.WallSerializer
    model_class = models.Wall

    def list(self, request, *args, **kwargs):
        return Response(self.generate_list(request))

    def create(self, request, *args, **kwargs):
        request.data['owner'] = request.user.id
        return super().create(request, *args, **kwargs)

    @classmethod
    def generate_list(cls, request):
        if not request.user.is_authenticated:
            return []

        walls_query = cls.generate_query_set(request).filter(owner=request.user)
        return cls.serializer_class(walls_query, many=True).data


class ContainerViewSet(CommonModelViewSet):
    serializer_class = serializers.ContainerSerializer
    model_class = models.Container


class SyncViewSet(CommonModelViewSet):

    def update(self, request, pk=None, *args, **kwargs):
        try:
            sync_id = request.data['sync_id']
        except KeyError:
            pass
        else:
            # Validate sync_id. Find any object that belong to user and has id equal to requested sync id
            if sync_id and not self.get_queryset().filter(pk=sync_id, container__wall__owner=request.user).exists():
                return JsonResponse({
                    'sync_id': [Public.Error.sync_id_miss_match]
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


class PortViewSet(SyncViewSet):
    serializer_class = serializers.PortSerializer
    model_class = models.Port

    def create(self, request, *args, **kwargs):
        request.data['owner'] = request.user.id
        return super().create(request, *args, **kwargs)


class SourceViewSet(CommonModelViewSet):
    parser_classes = (MultiPartParser,)
    model_class = models.Source
    serializer_class = serializers.SourceSerializer

    def create(self, request, *args, **kwargs):
        return HttpResponseForbidden()

    def list(self, request, *args, **kwargs):
        return HttpResponseForbidden()

    def get_object(self):
        return self.get_queryset().filter(id=self.kwargs.get('pk')).first()

    def retrieve(self, request, *args, **kwargs):
        try:
            source = self.get_object()
        except self.model_class.DoesNotExist:
            return HttpResponseNotFound()
        if source.file is None:
            return HttpResponseNotFound()
        return sendfile(request, MEDIA_BASE_PATH + '/' + source.file.name,
                        attachment=request.GET.get('attachment') is not None)

    def update(self, request, *args, **kwargs):
        try:
            source = self.get_object()
        except self.model_class.DoesNotExist:
            return HttpResponseNotFound()
        try:
            old_path = source.file.path
        except ValueError:
            old_path = None
        response = super().update(request, *args, **kwargs)
        for parent in source.parent.all():
            parent.propagate_instance_updated()
        try:
            os.remove(old_path)
        except (TypeError, OSError):
            pass
        return response

    def destroy(self, request, *args, **kwargs):
        # Delete file, not source object
        try:
            source = self.get_object()
        except self.model_class.DoesNotExist:
            return HttpResponseNotFound()
        source.delete_file()
        for parent in source.parent.all():
            parent.propagate_instance_updated()
        return Response('OK')


class DocumentViewSet(SyncViewSet):
    serializer_class = serializers.DocumentSerializer
    model_class = models.Document

    def create(self, request, *args, **kwargs):
        try:
            del request.data['source']
        except KeyError:
            pass
        response = super().create(request, *args, **kwargs)
        document = self.get_queryset().get(id=response.data['id'])
        source = models.Source()
        source.save()
        document.source = source
        document.save()
        return response

    def destroy(self, request, *args, **kwargs):
        document = self.get_queryset().get(id=kwargs['pk'])
        document.source.delete()
        return super().destroy(request, *args, **kwargs)
