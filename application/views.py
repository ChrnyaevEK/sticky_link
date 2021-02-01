from application import models
from application import serializers
from rest_framework import viewsets


class WallViewSet(viewsets.ModelViewSet):
    queryset = models.Wall.objects.all()
    serializer_class = serializers.WallSerializer


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
