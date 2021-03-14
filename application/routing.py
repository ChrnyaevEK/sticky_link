from django.urls import path

from application import consumers
websocket_urlpatterns = [
    path('wss/<int:id>', consumers.WallConsumer.as_asgi()),
]
