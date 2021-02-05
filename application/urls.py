from rest_framework import routers
from django.urls import path, include
from application import views

router = routers.DefaultRouter()
router.register('wall', views.WallViewSet)
router.register('simple_text', views.SimpleTextViewSet)
router.register('rich_text', views.RichTextViewSet)
router.register('url', views.URLViewSet)
router.register('simple_list', views.SimpleListViewSet)

urlpatterns = [
    path('api/', include(router.urls), name="api"),
    path('app/enter/', views.Enter.as_view(), name="enter"),
    path('app/leave/', views.Leave.as_view(), name="leave"),
]
