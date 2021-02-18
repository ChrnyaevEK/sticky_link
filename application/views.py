from application import models
from application import serializers
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from django.http import JsonResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import View
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

    @staticmethod
    def get_context(request):
        walls = _get_protected_queryset(models.Wall, request.user)
        return JsonResponse({
            'walls': serializers.WallSerializer(walls, many=True),
            'settings': serializers.ObjectSerializer(models.Settings).data,
            'user': serializers.UserSerializer(request.user).data,
        })


class WallViewSet(ModelViewSet):
    serializer_class = serializers.WallSerializer

    def get_queryset(self):
        return _get_protected_queryset(models.Wall, self.request.user)

    def get_context(self, request, wall_id):
        walls_query = self.get_queryset()
        try:
            wall = walls_query.get(pk=wall_id)
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
        return JsonResponse({
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
