from rest_framework import routers
from django.urls import path, include, re_path
from application import views
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register('wall', views.WallViewSet, basename='wall')
router.register('container', views.ContainerViewSet, basename='container')
router.register('simple_text', views.SimpleTextViewSet, basename='simple_text')
router.register('url', views.URLViewSet, 'url')
router.register('simple_list', views.SimpleListViewSet, basename='simple_list')
router.register('counter', views.CounterViewSet, basename='counter')
router.register('simple_switch', views.SimpleSwitchViewSet, basename='simple_switch')
router.register('port', views.PortViewSet, basename='port')
router.register('user', views.UserViewSet, basename='user')

urlpatterns = [
    path('', views.App.enter, name="enter"),
    path('port/<str:uid>/', views.App.port, name="port"),
    path('api/state/', views.App.state, name="state"),
    path('api/state/<int:wall_id>/', views.App.state, name="state"),
    path('api/', include(router.urls), name="api"),
    *static(settings.STATIC_URL, document_root='templates/application/dist/static'),
    re_path('.*', views.App.enter),
]
