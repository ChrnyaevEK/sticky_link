from channels.generic.websocket import AsyncWebsocketConsumer
import json


class Event:
    instance_update = 'on_instance_update'  # Or create
    instance_destroy = 'on_instance_destroy'


class WallConsumer(AsyncWebsocketConsumer):
    group_name = None

    @classmethod
    def generate_group_name(cls, wall_id):
        return str(wall_id)

    def __init__(self, *args, **kwargs):
        self.group_name = self.generate_group_name(self.scope['url_route']['kwargs']['id'])
        super().__init__(*args, **kwargs)

    async def connect(self):
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

    async def on_instance_update(self, data):
        await self.send(text_data=json.dumps(data))

    async def on_instance_destroy(self, data):
        await self.send(text_data=json.dumps(data))
