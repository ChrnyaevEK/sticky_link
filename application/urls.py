from rest_framework import routers
from django.urls import path, include
from application import views
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register('wall', views.WallViewSet, basename='wall')
router.register('simple_text', views.SimpleTextViewSet, basename='simple_text')
router.register('rich_text', views.RichTextViewSet, basename='rich_text')
router.register('url', views.URLViewSet, 'url')
router.register('simple_list', views.SimpleListViewSet, basename='simple_list')
router.register('counter', views.CounterViewSet, basename='counter')
router.register('user', views.UserViewSet, basename='user')

urlpatterns = [
    path('', views.Event.enter, name="enter"),
    path('api/', include(router.urls), name="api"),
    path('api/wall_context/<int:wall_id>/', views.WallViewSet.get_context, name="wall_context"),
    path('api/user_context/', views.UserViewSet.get_context, name="user_context"),
] + static(settings.STATIC_URL, document_root='templates/application/dist/static')
