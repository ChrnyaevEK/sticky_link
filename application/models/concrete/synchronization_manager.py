from django.db import models

from application.models.abstract import BaseFactory
from application.consumers import Event as ConsumerEvent, WallConsumer

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


class ConcreteFactory(BaseFactory):

    @classmethod
    def _get_base_class(cls, base):
        class Base(base):
            sync_fields = []
            sync_id = None

            class Meta:
                abstract = True

            def propagate_instance_updated(self):
                if self.related_wall_instance is not None:
                    channel_layer = get_channel_layer()
                    async_to_sync(channel_layer.group_send)(
                        WallConsumer.generate_group_name(self.related_wall_instance.id),
                        {
                            'type': ConsumerEvent.instance_update,
                            'instance': {
                                'type': self.type,
                                'id': self.id,
                                'uid': self.uid,
                                'version': self.version,
                            },
                        })

            def propagate_instance_deleted(self):
                if self.related_wall_instance is not None:
                    channel_layer = get_channel_layer()
                    async_to_sync(channel_layer.group_send)(
                        WallConsumer.generate_group_name(self.related_wall_instance.id),
                        {
                            'type': ConsumerEvent.instance_destroy,
                            'instance': {
                                'type': self.type,
                                'id': self.id,
                                'uid': self.uid,
                            }
                        })

            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.prevent_synchronization = False

            def synchronize_bounded_instances(self):
                if not self.prevent_synchronization:
                    bounded = self.__class__.objects.filter(sync_id=self)
                    if self.sync_id is not None:
                        bounded = bounded | self.__class__.objects.filter(pk=self.sync_id.id)
                    for instance in bounded:
                        instance.prevent_synchronization = True
                        if instance != self:
                            for field in instance.sync_fields:
                                instance.__setattr__(field, self.__getattribute__(field))
                            instance.save()

            @property
            def is_referenced(self):
                return self.__class__.objects.filter(sync_id=self).exists()

        return Base

    @classmethod
    def get_wall_class(cls, base):
        class Wall(cls._get_base_class(base)):
            sync_fields = ['allow_anonymous_view', 'lock_widgets']
            sync_id = models.ForeignKey('Wall', blank=True, null=True, on_delete=models.SET_NULL)

            class Meta:
                abstract = True

        return Wall

    @classmethod
    def get_container_class(cls, base):
        class Container(cls._get_base_class(base)):
            sync_fields = ['h', 'w']
            sync_id = models.ForeignKey('Container', blank=True, null=True, on_delete=models.SET_NULL)

            class Meta:
                abstract = True

        return Container

    @classmethod
    def get_port_class(cls, base):
        class Port(cls._get_base_class(base)):
            sync_fields = ['activated', 'authenticated_wall', 'anonymous_wall', 'redirect_url']
            sync_id = models.ForeignKey('Port', blank=True, null=True, on_delete=models.SET_NULL)

            class Meta:
                abstract = True

        return Port

    @classmethod
    def get_source_class(cls, base):
        class Source(cls._get_base_class(base)):
            sync_fields = []
            sync_id = models.ForeignKey('Source', blank=True, null=True, on_delete=models.SET_NULL)

            def propagate_instance_updated(self):
                for document in self.document_set.all():
                    document.propagate_instance_updated()
                for image in self.image_set.all():
                    image.propagate_instance_updated()

            class Meta:
                abstract = True

        return Source

    @classmethod
    def get_simple_text_class(cls, base):
        class SimpleText(cls._get_base_class(base)):
            sync_fields = ['text_content']
            sync_id = models.ForeignKey('SimpleText', blank=True, null=True, on_delete=models.SET_NULL)

            class Meta:
                abstract = True

        return SimpleText

    @classmethod
    def get_url_class(cls, base):
        class URL(cls._get_base_class(base)):
            sync_fields = ['href', 'text', 'open_in_new_window']
            sync_id = models.ForeignKey('URL', blank=True, null=True, on_delete=models.SET_NULL)

            class Meta:
                abstract = True

        return URL

    @classmethod
    def get_image_class(cls, base):
        class Image(cls._get_base_class(base)):
            sync_fields = ['source', 'alt']
            sync_id = models.ForeignKey('Image', blank=True, null=True, on_delete=models.SET_NULL)

            class Meta:
                abstract = True

        return Image

    @classmethod
    def get_video_class(cls, base):
        class Video(cls._get_base_class(base)):
            sync_fields = ['source', 'autoplay', 'loop', 'youtube']
            sync_id = models.ForeignKey('Video', blank=True, null=True, on_delete=models.SET_NULL)

            class Meta:
                abstract = True

        return Video

    @classmethod
    def get_simple_list_class(cls, base):
        class SimpleList(cls._get_base_class(base)):
            sync_fields = ['items', 'inner_border']
            sync_id = models.ForeignKey('SimpleList', blank=True, null=True, on_delete=models.SET_NULL)

            class Meta:
                abstract = True

        return SimpleList

    @classmethod
    def get_counter_class(cls, base):
        class Counter(cls._get_base_class(base)):
            sync_fields = ['value', 'vertical', 'step']
            sync_id = models.ForeignKey('Counter', blank=True, null=True, on_delete=models.SET_NULL)

            class Meta:
                abstract = True

        return Counter

    @classmethod
    def get_simple_switch_class(cls, base):
        class SimpleSwitch(cls._get_base_class(base)):
            sync_fields = ['value']
            sync_id = models.ForeignKey('SimpleSwitch', blank=True, null=True, on_delete=models.SET_NULL)

            class Meta:
                abstract = True

        return SimpleSwitch

    @classmethod
    def get_document_class(cls, base):
        class Document(cls._get_base_class(base)):
            sync_fields = ['source']
            sync_id = models.ForeignKey('Document', blank=True, null=True, on_delete=models.SET_NULL)

            class Meta:
                abstract = True

        return Document
