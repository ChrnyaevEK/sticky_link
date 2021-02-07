from application import models
from application import serializers
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from django.http import JsonResponse, Http404
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from sticky_link import env
from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.core.exceptions import PermissionDenied


# Entry point for users - resolve on enter redirections, return client app
class Enter(View):
    template = 'application/dist/index.html'

    def get(self, request):
        return HttpResponse(render(request, self.template))


# Exit point - resolve on exit redirections
class Leave(View):
    def get(self, request):
        pass


class ProfileView(View):
    @staticmethod
    def get(request):
        if request.user.is_authenticated:
            return JsonResponse({
                'user': serializers.UserSerializer(request.user).data,
                'settings': serializers.ObjectSerializer(models.Settings).data
            })
        else:
            raise Http404


class WallViewSet(ModelViewSet):
    serializer_class = serializers.WallSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [] if env.DEBUG else [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return models.Wall.objects.filter(owner=self.request.user) | self.request.user.related_walls.all()
        else:
            return models.Wall.objects.filter(allowed_anonymous=True)

    def retrieve(self, request, pk=None, *args, **kwargs):
        query = self.get_queryset()
        try:
            wall = query.get(pk=pk)
        except models.Wall.DoesNotExist:
            try:  # Check if wall exit
                models.Wall.objects.get(pk=pk)
            except models.Wall.DoesNotExist:
                raise Http404  # Wall does not exist at all
            else:
                raise PermissionDenied  # Wall exist, but access is not granted
        else:
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
            })

    # def list(self, request, *args, **kwargs) - default behaviour

    # def create(self, request, *args, **kwargs) - default behaviour

    def update(self, request, pk=None, *args, **kwargs):
        # Do nothing (yet)
        pass

    def partial_update(self, request, pk=None, *args, **kwargs):
        # Do nothing (yet)
        pass

    # def destroy(self, request, pk=None, *args, **kwargs) - default behaviour


class SimpleTextViewSet(ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [] if env.DEBUG else [IsAuthenticated]
    queryset = models.SimpleText.objects.all()
    serializer_class = serializers.SimpleTextSerializer


class RichTextViewSet(ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [] if env.DEBUG else [IsAuthenticated]
    queryset = models.RichText.objects.all()
    serializer_class = serializers.RichTextSerializer


class URLViewSet(ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [] if env.DEBUG else [IsAuthenticated]
    queryset = models.URL.objects.all()
    serializer_class = serializers.URLSerializer


class SimpleListViewSet(ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [] if env.DEBUG else [IsAuthenticated]
    queryset = models.SimpleList.objects.all()
    serializer_class = serializers.SimpleListSerializer


class CounterViewSet(ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [] if env.DEBUG else [IsAuthenticated]
    queryset = models.Counter.objects.all()
    serializer_class = serializers.CounterSerializer
