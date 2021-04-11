from django.urls import path

from application import consumers
websocket_urlpatterns = [
    path('wss/<str:id>', consumers.WallConsumer.as_asgi()),
]
