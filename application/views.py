from application import models
from application import serializers
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from sticky_link import env
from django.shortcuts import render
from django.http import HttpResponse
from django.views import View


# Entry point for users - resolve on enter redirections, return client app
class Enter(View):
    template = 'application/dist/index.html'

    def get(self, request):
        return HttpResponse(render(request, self.template))


# Exit point - resolve on exit redirections
class Leave(View):
    def get(self, request):
        pass


class WallViewSet(viewsets.ModelViewSet):
    queryset = models.Wall.objects.all()
    serializer_class = serializers.WallSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [] if env.DEBUG else [IsAuthenticated]

    def retrieve(self, request, pk=None, *args, **kwargs):
        wall = get_object_or_404(models.Wall, pk=pk)
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
            'wall': self.serializer_class(wall).data,
            'widgets': widgets,
            'settings': serializers.ObjectSerializer(models.Settings).data
        })


class SimpleTextViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [] if env.DEBUG else [IsAuthenticated]
    queryset = models.SimpleText.objects.all()
    serializer_class = serializers.SimpleTextSerializer


class RichTextViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [] if env.DEBUG else [IsAuthenticated]
    queryset = models.RichText.objects.all()
    serializer_class = serializers.RichTextSerializer


class URLViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [] if env.DEBUG else [IsAuthenticated]
    queryset = models.URL.objects.all()
    serializer_class = serializers.URLSerializer


class SimpleListViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [] if env.DEBUG else [IsAuthenticated]
    queryset = models.SimpleList.objects.all()
    serializer_class = serializers.SimpleListSerializer


class CounterViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [] if env.DEBUG else [IsAuthenticated]
    queryset = models.Counter.objects.all()
    serializer_class = serializers.CounterSerializer
