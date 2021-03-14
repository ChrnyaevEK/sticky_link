from application import models
from application import serializers
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from django.http import JsonResponse, Http404
from django.shortcuts import render
from rest_framework.response import Response
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from channels.layers import get_channel_layer
from application.consumers import Event as ConsumerEvent, WallConsumer
from asgiref.sync import async_to_sync


def _get_protected_queryset(model, user, consider_anonymous_access=False):
    if model == models.Wall:
        return model.objects.filter(owner=user)
    return model.objects.filter(wall__owner=user)


class Event:
    @staticmethod
    def enter(request):
        # Entry point for users - resolve on enter redirections, return client app
        template = 'application/dist/index.html'
        return HttpResponse(render(request, template))


class Static:
    @staticmethod
    def settings(request):
        return JsonResponse(serializers.ObjectSerializer(models.Settings).data)


class UserViewSet(ReadOnlyModelViewSet):
    serializer_class = serializers.UserSerializer

    def get_queryset(self):
        return models.User.objects.filter(pk=self.request.user.id)

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

    def retrieve(self, request, pk=None):
        walls_query = _get_protected_queryset(models.Wall, request.user)  # Retrieve only!
        try:
            wall = walls_query.get(pk=pk)
        except models.Wall.DoesNotExist:
            raise PermissionDenied  # Wall exist, but access is not granted
        widgets = []
        for model, serializer in (
                (models.SimpleText, serializers.SimpleTextSerializer),
                (models.URL, serializers.URLSerializer),
                (models.SimpleList, serializers.SimpleListSerializer),
                (models.Counter, serializers.CounterSerializer),
        ):
            for widget in model.objects.filter(wall=wall):
                widgets.append(serializer(widget).data)
        wall = self.serializer_class(wall).data
        wall['widgets'] = widgets
        return Response(wall)


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
