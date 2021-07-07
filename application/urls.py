from rest_framework import routers
from django.urls import path, include, re_path
from application import views
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter(trailing_slash=False)
router.register('wall', views.WallViewSet, basename='wall')
router.register('container', views.ContainerViewSet, basename='container')
router.register('simple_text', views.SimpleTextViewSet, basename='simple_text')
router.register('url', views.URLViewSet, 'url')
router.register('image', views.ImageViewSet, 'image')
router.register('video', views.VideoViewSet, 'video')
router.register('simple_list', views.SimpleListViewSet, basename='simple_list')
router.register('counter', views.CounterViewSet, basename='counter')
router.register('simple_switch', views.SimpleSwitchViewSet, basename='simple_switch')
router.register('document', views.DocumentViewSet, basename='document')
router.register('port', views.PortViewSet, basename='port')
router.register('source', views.SourceViewSet, basename='source')

urlpatterns = [
    path('', views.App.enter, name="enter"),
    # Slash should be here - catch both with slash and without with APPEND_SLASH setting
    path('port/<str:pk>/', views.App.port, name="port"),
    path('api/state', views.App.state, name="state"),
    path('api/state/<str:pk>', views.App.state, name="state"),
    path('api/trusted_user', views.App.trusted_user),
    path('api/wall/copy/<str:pk>', views.App.copy_wall),
    path('api/container/copy/<str:pk>', views.App.copy_container),
    path('api/', include(router.urls), name="api"),
    *static(settings.STATIC_URL, document_root='templates/application/dist/static'),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    re_path('.*', views.App.enter),
]
