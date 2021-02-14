from rest_framework import routers
from django.urls import path, include
from application import views
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register('wall', views.WallViewSet, basename='wall')
router.register('simple_text', views.SimpleTextViewSet)
router.register('rich_text', views.RichTextViewSet)
router.register('url', views.URLViewSet)
router.register('simple_list', views.SimpleListViewSet)
router.register('counter', views.CounterViewSet)
router.register('user', views.UserView, basename='user')

urlpatterns = [
    path('', views.Enter.as_view(), name="application"),
    path('api/', include(router.urls), name="api"),
] + static(settings.STATIC_URL, document_root='templates/application/dist/static')
