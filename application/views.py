from application import models
from application import serializers
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from django.http import JsonResponse, Http404
from django.shortcuts import render
from rest_framework.response import Response
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from channels.layers import get_channel_layer
from application.consumers import Event as ConsumerEvent
from asgiref.sync import async_to_sync
import hashlib
import json


def _get_protected_queryset(model, user):
    if model == models.Wall:
        return model.objects.filter(owner=user)
    return model.objects.filter(wall__owner=user)


class Event:
    @staticmethod
    def enter(request):
        # Entry point for users - resolve on enter redirections, return client app
        template = 'application/dist/index.html'
        return HttpResponse(render(request, template))


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
        walls = _get_protected_queryset(models.Wall, request.user)
        return JsonResponse({
            'walls': serializers.WallSerializer(walls, many=True).data,
            'settings': serializers.ObjectSerializer(models.Settings).data,
            'user': serializers.UserSerializer(request.user).data,
        })


class CustomModelViewSet(ModelViewSet):
    channel_layer = get_channel_layer()
    version_hash_field = 'version_hash'

    def ensure_update_synchronization(self, response):
        data = response.data
        try:
            wall_id = data['wall']
        except KeyError:
            wall_id = data['id']
        version_hash = self._get_version_hash(data)
        async_to_sync(self.channel_layer.group_send)(
            f'{models.Wall.type}_{wall_id}',
            {
                'type': ConsumerEvent.wall_update,
                'instance': {
                    'type': data['type'],
                    'id': data['id'],
                    self.version_hash_field: version_hash,
                }
            })
        response.data[self.version_hash_field] = version_hash

    @staticmethod
    def _get_version_hash(validated_data):
        return hashlib.md5(json.dumps(validated_data).encode('utf-8')).hexdigest()

    @staticmethod
    def _check_update_fields(validated_data, fields):
        return len(set(validated_data.keys()).intersection(fields))

    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)
        self.ensure_update_synchronization(response)
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        self.ensure_update_synchronization(response)
        return response


class WallViewSet(CustomModelViewSet):
    serializer_class = serializers.WallSerializer

    def get_queryset(self):
        return _get_protected_queryset(models.Wall, self.request.user)

    def retrieve(self, request, pk=None):
        walls_query = _get_protected_queryset(models.Wall, request.user)
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
        return Response({
            'wall': serializers.WallSerializer(wall).data,
            'widgets': widgets,
        })


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
