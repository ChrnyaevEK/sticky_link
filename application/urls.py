from rest_framework import routers
from django.urls import path, include, re_path
from application import views
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register('wall', views.WallViewSet, basename='wall')
router.register('simple_text', views.SimpleTextViewSet, basename='simple_text')
router.register('url', views.URLViewSet, 'url')
router.register('simple_list', views.SimpleListViewSet, basename='simple_list')
router.register('counter', views.CounterViewSet, basename='counter')
router.register('switch', views.SwitchViewSet, basename='switch')
router.register('user', views.UserViewSet, basename='user')

urlpatterns = [
    path('', views.Event.enter, name="enter"),
    path('api/settings/', views.Static.settings, name="static_settings"),
    path('api/', include(router.urls), name="api"),
    *static(settings.STATIC_URL, document_root='templates/application/dist/static'),
    re_path('.*', views.Event.enter, name="enter"),
]
