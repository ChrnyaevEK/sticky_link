from channels.generic.websocket import AsyncWebsocketConsumer
from application.models import Wall
import json


class Event:
    wall_update = 'on_wall_update'


class WallConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.group_name = f"{Wall.Default.type}_{self.scope['url_route']['kwargs']['id']}"
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
        data = data['instance']
        # Do not send notifications to the changes source client
        if data['ip'] != self.scope['client'][0] and data['user'] != self.scope['user'].id:
            await self.send(text_data=json.dumps(data))
