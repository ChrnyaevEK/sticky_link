import hashlib
import json
from channels.layers import get_channel_layer
from application.consumers import Event as ConsumerEvent, WallConsumer
from asgiref.sync import async_to_sync


def get_version(instance):
    version_string = ''
    try:
        version_string = instance.last_update.isoformat()
    except AttributeError:
        pass
    return hashlib.md5(json.dumps(version_string).encode('utf-8')).hexdigest()


def get_wall_id(instance):
    try:  # Container or Port
        return instance.wall.id
    except AttributeError:
        try:  # Any widget
            return instance.container.wall.id
        except AttributeError:  # Wall it self
            return instance.id


def push_instance_update(instance):
    wall_id = get_wall_id(instance)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        WallConsumer.generate_group_name(wall_id),
        {
            'type': ConsumerEvent.instance_update,
            'instance': {
                'type': instance.type,
                'id': instance.id,
                'uid': instance.uid(),
                'version': get_version(instance),
            },
        })


def push_instance_destroy(instance):
    wall_id = get_wall_id(instance)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        WallConsumer.generate_group_name(wall_id),
        {
            'type': ConsumerEvent.instance_destroy,
            'instance': {
                'type': instance.type,
                'id': instance.id,
                'uid': instance.uid(),
            }
        })
