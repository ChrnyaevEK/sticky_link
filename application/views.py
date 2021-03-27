from application import models
from application import serializers
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.response import Response
from django.http import HttpResponse
from channels.layers import get_channel_layer
from application.consumers import Event as ConsumerEvent, WallConsumer
from asgiref.sync import async_to_sync
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated


def _get_protected_queryset(model, user):
    if model == models.Wall:
        q = Q(allow_anonymous_view=True)
        if not user.is_anonymous:
            q.add(Q(owner=user), Q.OR)
    elif model == models.Container:
        q = Q(wall__allow_anonymous_view=True)
        if not user.is_anonymous:
            q.add(Q(wall__owner=user), Q.OR)
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
    @api_view(http_method_names=['GET'])
    def state(request, wall_id=None):
        try:
            wall = _get_protected_queryset(models.Wall, request.user).get(pk=wall_id)
        except models.Wall.DoesNotExist:
            wall = None
            containers = None
            container = None
            widgets = None
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
                ):
                    for widget in model.objects.filter(container=container):
                        widgets.append(serializer(widget).data)
                containers.append(serializers.ContainerSerializer(container).data)
            if not containers:
                container = models.Container(wall=wall, index=0)
                container.save()
                containers = [serializers.ContainerSerializer(container).data]
            container = containers[0]
            wall = serializers.WallSerializer(wall).data
        return JsonResponse({
            'user': serializers.UserSerializer(request.user).data,
            'wall': wall,
            'containers': containers,
            'container': container,
            'widgets': widgets,
            'walls': WallViewSet.get_list(request) or None
        })


class UserViewSet(ReadOnlyModelViewSet):
    serializer_class = serializers.UserSerializer

    def retrieve(self, request, *args, **kwargs):
        return self._get(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        return self._get(request, *args, **kwargs)

    @staticmethod
    def _get(request, *args, **kwargs):
        return JsonResponse(serializers.UserSerializer(request.user).data)


class CustomModelViewSet(ModelViewSet):
    channel_layer = get_channel_layer()
    version_hash_field = 'version'

    def push_instance_update(self, response):
        data = response.data
        try:
            wall_id = data['wall']
        except KeyError:
            wall_id = data['id']
        async_to_sync(self.channel_layer.group_send)(
            WallConsumer.generate_group_name(wall_id),
            {
                'type': ConsumerEvent.instance_update,
                'instance': {
                    'type': data['type'],
                    'id': data['id'],
                    'uid': data['uid'],
                    'version': data['version'],
                },
            })

    def push_instance_destroy(self, instance):
        try:
            wall_id = instance.wall.id
        except AttributeError:
            wall_id = instance.id
        async_to_sync(self.channel_layer.group_send)(
            WallConsumer.generate_group_name(wall_id),
            {
                'type': ConsumerEvent.instance_destroy,
                'instance': {
                    'type': instance.type,
                    'id': instance.id,
                    'uid': instance.uid(),
                }
            })

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ('list', 'retrieve', 'partial_update', 'update'):
            permission_classes = []
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        self.push_instance_update(response)
        return response

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        self.push_instance_update(response)
        return response

    def destroy(self, request, *args, **kwargs):
        instance = self.get_queryset().get(pk=kwargs['pk'])
        response = super().destroy(request, *args, **kwargs)
        self.push_instance_destroy(instance)
        return response


class WallViewSet(CustomModelViewSet):
    serializer_class = serializers.WallSerializer

    def get_queryset(self):
        return _get_protected_queryset(models.Wall, self.request.user)

    def list(self, request, *args, **kwargs):
        return Response(self.get_list(request))

    @classmethod
    def get_list(cls, request):
        if request.user.is_authenticated:
            walls_query = _get_protected_queryset(models.Wall, request.user).filter(owner=request.user)
            return cls.serializer_class(walls_query, many=True).data
        else:
            return []


class ContainerViewSet(CustomModelViewSet):
    serializer_class = serializers.ContainerSerializer

    def get_queryset(self):
        return _get_protected_queryset(models.Container, self.request.user)


class SimpleTextViewSet(CustomModelViewSet):
    serializer_class = serializers.SimpleTextSerializer

    def get_queryset(self):
        return _get_protected_queryset(models.SimpleText, self.request.user)


class URLViewSet(CustomModelViewSet):
    serializer_class = serializers.URLSerializer

    def get_queryset(self):
        return _get_protected_queryset(models.URL, self.request.user)


class SimpleListViewSet(CustomModelViewSet):
    serializer_class = serializers.SimpleListSerializer

    def get_queryset(self):
        return _get_protected_queryset(models.SimpleList, self.request.user)


class CounterViewSet(CustomModelViewSet):
    serializer_class = serializers.CounterSerializer

    def get_queryset(self):
        return _get_protected_queryset(models.Counter, self.request.user)


class SimpleSwitchViewSet(CustomModelViewSet):
    serializer_class = serializers.SimpleSwitchSerializer

    def get_queryset(self):
        return _get_protected_queryset(models.SimpleSwitch, self.request.user)
