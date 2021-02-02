from application import models
from application import serializers
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from django.http import JsonResponse


class WallViewSet(viewsets.ModelViewSet):
    queryset = models.Wall.objects.all()
    serializer_class = serializers.WallSerializer

    def retrieve(self, request, pk=None, *args, **kwargs):
        wall = get_object_or_404(models.Wall, pk=pk)
        widgets = []
        for model, serializer in (
                (models.SimpleText, serializers.SimpleTextSerializer),
                (models.RichText, serializers.RichTextSerializer),
                (models.URL, serializers.URLSerializer),
                (models.SimpleList, serializers.SimpleListSerializer),
        ):
            for widget in model.objects.filter(wall=wall):
                widgets.append(serializer(widget).data)
        return JsonResponse({
            'wall': self.serializer_class(wall).data,
            'widgets': widgets,
        })


class SimpleTextViewSet(viewsets.ModelViewSet):
    queryset = models.SimpleText.objects.all()
    serializer_class = serializers.SimpleTextSerializer


class RichTextViewSet(viewsets.ModelViewSet):
    queryset = models.RichText.objects.all()
    serializer_class = serializers.RichTextSerializer


class URLViewSet(viewsets.ModelViewSet):
    queryset = models.URL.objects.all()
    serializer_class = serializers.URLSerializer


class SimpleListViewSet(viewsets.ModelViewSet):
    queryset = models.SimpleList.objects.all()
    serializer_class = serializers.SimpleListSerializer
