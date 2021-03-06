from channels.generic.websocket import AsyncWebsocketConsumer
from application.models import Wall
import json


class Event:
    wall_update = 'on_wall_update'


class WallConsumer(AsyncWebsocketConsumer):
    @staticmethod
    def generate_group_name(wall_id):
        return f"{Wall.Default.type}_{wall_id}"

    async def connect(self):
        self.group_name = self.generate_group_name(self.scope['url_route']['kwargs']['id'])
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name,
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def on_wall_update(self, data):
        await self.send(text_data=json.dumps(data))
