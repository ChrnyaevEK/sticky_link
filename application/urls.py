from rest_framework import routers
from django.urls import path, include
from application.views import SimpleTextViewSet

router = routers.DefaultRouter()
router.register('simple_text', SimpleTextViewSet)

urlpatterns = [
    path('', include(router.urls))
]
