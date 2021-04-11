from application import models
from application import serializers
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.decorators import api_view
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated


def _get_protected_queryset(model, user):
    if model == models.Wall:
        q = Q(allow_anonymous_view=True)
        if not user.is_anonymous:
            q.add(Q(owner=user), Q.OR)
    elif model == models.Container or model == models.Port:
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
    def port(request, uid):
        """ Resolve redirection to required resource """
        try:
            port = models.Port.objects.get(pk=uid)
        except models.Port.DoesNotExist:
            return HttpResponseNotFound('Port does not exist')
        port.visited += 1
        port.save()
        if port.wall is None:
            return HttpResponseNotFound('Port refer invalid resource')
        return redirect(f'/wall/view/{port.wall.id}/')

    @staticmethod
    @api_view(http_method_names=['GET'])
    def state(request, wall_id=None):
        try:
            wall = _get_protected_queryset(models.Wall, request.user).get(pk=wall_id)
        except models.Wall.DoesNotExist:
            wall = None
            containers = []
            widgets = []
            ports = []
            meta = None
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
            meta = {
                'edit_permission': wall.owner == request.user,
                'view_permission': wall.allow_anonymous_view or wall.owner == request.user
            }
            ports = _get_protected_queryset(models.Port, request.user).filter(wall=wall)
            ports = serializers.PortSerializer(ports, many=True).data
            wall = serializers.WallSerializer(wall).data
        walls = WallViewSet.get_list(request)
        if not walls and wall:
            walls = [wall]
        elif not walls:
            walls = []

        user = serializers.UserSerializer(request.user).data
        if request.user.is_anonymous:
            user['username'] = 'anonymous'
        return JsonResponse({
            'user': user,
            'meta': meta,
            'containers': containers,
            'ports': ports,
            'widgets': widgets,
            'walls': walls
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

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ('list', 'retrieve', 'partial_update', 'update'):
            permission_classes = []
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def update(self, request, pk=None, *args, **kwargs):
        try:
            sync_id = request.data['sync_id']
        except KeyError:
            pass
        else:
            # Validate sync_id. Find any object that belong to user and has id equal to requested sync id
            if sync_id and not self.get_queryset().filter(pk=sync_id, container__wall__owner=request.user).exists():
                return JsonResponse({
                    'sync_id': ['Make sure the sync ID belong to user and widgets have the same type.']
                }, status=400)
        return super().update(request, *args, **kwargs)


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


class PortViewSet(CustomModelViewSet):
    serializer_class = serializers.PortSerializer

    def get_queryset(self):
        return _get_protected_queryset(models.Port, self.request.user)
