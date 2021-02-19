from application import models
from application import serializers
from rest_framework.decorators import permission_classes, api_view
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse, Http404
from django.shortcuts import render
from rest_framework.response import Response
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied


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


class WallViewSet(ModelViewSet):
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
                (models.RichText, serializers.RichTextSerializer),
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


class SimpleTextViewSet(ModelViewSet):
    serializer_class = serializers.SimpleTextSerializer

    def get_queryset(self):
        return _get_protected_queryset(models.SimpleText, self.request.user)


class RichTextViewSet(ModelViewSet):
    serializer_class = serializers.RichTextSerializer

    def get_queryset(self):
        return _get_protected_queryset(models.RichText, self.request.user)


class URLViewSet(ModelViewSet):
    serializer_class = serializers.URLSerializer

    def get_queryset(self):
        return _get_protected_queryset(models.URL, self.request.user)


class SimpleListViewSet(ModelViewSet):
    serializer_class = serializers.SimpleListSerializer

    def get_queryset(self):
        return _get_protected_queryset(models.SimpleList, self.request.user)


class CounterViewSet(ModelViewSet):
    serializer_class = serializers.CounterSerializer

    def get_queryset(self):
        return _get_protected_queryset(models.Counter, self.request.user)
