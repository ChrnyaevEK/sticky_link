from application import models
from application import serializers
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from django.http import JsonResponse, Http404
from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.core.exceptions import PermissionDenied


# Entry point for users - resolve on enter redirections, return client app
class Enter(View):
    template = 'application/dist/index.html'

    def get(self, request):
        return HttpResponse(render(request, self.template))


class UserView(ReadOnlyModelViewSet):
    serializer_class = serializers.UserSerializer

    def get_queryset(self):
        return models.User.objects.filter(pk=self.request.user.id)


class WallViewSet(ModelViewSet):
    serializer_class = serializers.WallSerializer

    def get_queryset(self):
        return models.Wall.objects.filter(owner=self.request.user)  # | self.request.user.related_walls.all()

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


class SimpleTextViewSet(ModelViewSet):
    queryset = models.SimpleText.objects.all()
    serializer_class = serializers.SimpleTextSerializer


class RichTextViewSet(ModelViewSet):
    queryset = models.RichText.objects.all()
    serializer_class = serializers.RichTextSerializer


class URLViewSet(ModelViewSet):
    queryset = models.URL.objects.all()
    serializer_class = serializers.URLSerializer


class SimpleListViewSet(ModelViewSet):
    queryset = models.SimpleList.objects.all()
    serializer_class = serializers.SimpleListSerializer


class CounterViewSet(ModelViewSet):
    queryset = models.Counter.objects.all()
    serializer_class = serializers.CounterSerializer
