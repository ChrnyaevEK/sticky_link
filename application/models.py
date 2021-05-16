"""
    Wall is a collection of Widgets. Each Widget has it's table and API.
    Walls are located in a different table and Wall id is a primary key for Widgets.
    Relay on ID's given by default
"""
import re
from django.db import models
from django.core.validators import BaseValidator, MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from hashid_field import HashidAutoField
from channels.layers import get_channel_layer
from application.consumers import Event as ConsumerEvent, WallConsumer
from asgiref.sync import async_to_sync
import hashlib
import logging

logger = logging.getLogger(__name__)


def _to_hash(sting):
    return hashlib.md5(sting.encode('utf-8')).hexdigest()


class Base(models.Model):
    type = None

    id = HashidAutoField(primary_key=True)

    date_of_creation = models.DateTimeField(verbose_name='Date of creation', auto_now_add=True)
    last_update = models.DateTimeField(verbose_name='Date of last update (wall or any widget)', auto_now=True)

    protected_fields = {'id', 'uid', 'version', 'type', 'date_of_creation', 'last_update'}

    def __str__(self):
        return f'{type(self).__name__}: {self.id}'

    class Meta:
        abstract = True

    @property
    def related_wall_instance(self):
        try:  # Container or Port
            return self.wall
        except AttributeError:
            try:  # Any widget
                return self.container.wall
            except AttributeError:  # Wall it self
                return self

    @property
    def uid(self):
        return _to_hash(f'{self.type}{self.id}')

    @property
    def version(self):
        return _to_hash(self.last_update.isoformat())



class SyncManager(Base):
    sync_fields = []
    sync_id = None

    def propagate_instance_updated(self):
        logger.info(f'Propagate instance update: {self}')
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
        logger.info(f'Propagate instance delete: {self}')
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
            logger.info(f'Sync bounded instances with: {self}')
            bounded = self.__class__.objects.filter(sync_id=self)
            if self.sync_id is not None:
                bounded = bounded | self.__class__.objects.filter(pk=self.sync_id.id)
            for instance in bounded:
                logger.info(f'Sync for: {instance}')
                instance.prevent_synchronization = True
                if instance != self:
                    for field in instance.sync_fields:
                        instance.__setattr__(field, self.__getattribute__(field))
                    instance.save()

    class Meta:
        abstract = True


class Wall(SyncManager):
    type = 'wall'

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    allow_anonymous_view = models.BooleanField('Allow anonymous view mode', default=False)
    title = models.CharField(verbose_name='Wall title', max_length=200, default='Untitled', null=True, blank=True)
    description = models.CharField(verbose_name='Wall description', max_length=500, blank=True, null=True)
    lock_widgets = models.BooleanField(verbose_name='Lock widgets at wall', default=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.propagate_instance_updated()

    def delete(self, *args, **kwargs):
        self.propagate_instance_deleted()
        super().delete(*args, **kwargs)

    @classmethod
    def validate_anonymous_access(cls, accessed_fields):
        protected_fields = {'owner', 'allowed_users', 'allow_anonymous_view', 'title', 'description', 'lock_widgets'}
        protected_fields.update(cls.protected_fields)
        return not protected_fields.intersection(accessed_fields)


class Container(SyncManager):
    type = 'container'

    wall = models.ForeignKey(Wall, on_delete=models.CASCADE)
    index = models.IntegerField(verbose_name='Index of container in wall', validators=[MinValueValidator(0)])

    h = models.IntegerField(verbose_name='Container height', default=100, validators=[MinValueValidator(50)])
    w = models.IntegerField(verbose_name='Container width', default=2000)  # Should not change (is static)

    title = models.CharField(verbose_name='Container title', max_length=200, null=True, blank=True)
    description = models.CharField(verbose_name='Container description', max_length=500, blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.propagate_instance_updated()

    def delete(self, *args, **kwargs):
        self.propagate_instance_deleted()
        super().delete(*args, **kwargs)

    @classmethod
    def validate_anonymous_access(cls, accessed_fields):
        protected_fields = {'wall', 'index', 'h', 'w', 'description', 'title'}
        protected_fields.update(cls.protected_fields)
        return not protected_fields.intersection(accessed_fields)


class ColorValidator(BaseValidator):
    regex = re.compile(r'^#[0-9a-fA-F]{8}$|#[0-9a-fA-F]{6}$|#[0-9a-fA-F]{4}$|#[0-9a-fA-F]{3}$')  # ARGB hex color

    def compare(self, a, b):
        return self.regex.match(a)


class Widget(SyncManager):
    title = models.CharField(max_length=200, blank=True, null=True)
    description = models.CharField(verbose_name='Widget description', max_length=500, blank=True, null=True)

    container = models.ForeignKey(Container, on_delete=models.CASCADE)
    help = models.CharField(max_length=200, null=True, blank=True)

    w = models.IntegerField(verbose_name='Widget width', default=200, validators=[MinValueValidator(50)])
    h = models.IntegerField(verbose_name='Widget height', default=100, validators=[MinValueValidator(50)])
    z = models.IntegerField(verbose_name='Widget z index(stack position)', default=0,
                            validators=[MaxValueValidator(100), MinValueValidator(0)])
    x = models.IntegerField(verbose_name='Offset left from parent', default=0, validators=[MinValueValidator(0)])
    y = models.IntegerField(verbose_name='Offset top from parent', default=0, validators=[MinValueValidator(0)])

    font_size = models.IntegerField(verbose_name='Widget font size', default=14,
                                    validators=[MaxValueValidator(40), MinValueValidator(6)])
    font_weight = models.IntegerField(verbose_name='Widget font weight', default=400,
                                      validators=[MaxValueValidator(900), MinValueValidator(100)])

    background_color = models.CharField(max_length=9, validators=[ColorValidator], default='#ffffff')
    text_color = models.CharField(max_length=9, validators=[ColorValidator], default='#000000')

    border = models.BooleanField(default=True)

    @classmethod
    def validate_anonymous_access(cls, accessed_fields):
        protected_fields = {'font_size', 'font_weight', 'background_color', 'text_color', 'border', 'help', 'w', 'h',
                            'z', 'x', 'y', 'sync_fields', 'container', 'owner'}
        protected_fields.update(cls.protected_fields)
        return not protected_fields.intersection(accessed_fields)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.propagate_instance_updated()
        self.synchronize_bounded_instances()

    def delete(self, *args, **kwargs):
        self.propagate_instance_deleted()
        for widget in self.__class__.objects.filter(sync_id=self):
            widget.propagate_instance_updated()
        super().delete(*args, **kwargs)

    @property
    def is_referenced(self):
        return self.__class__.objects.filter(sync_id=self).exists()

    class Meta:
        abstract = True


class SimpleText(Widget):
    type = 'simple_text'
    sync_fields = ['text_content']

    sync_id = models.ForeignKey('SimpleText', blank=True, null=True, on_delete=models.SET_NULL)
    text_content = models.TextField(verbose_name='Text content of widget', null=True, blank=True)


class URL(Widget):
    type = 'url'
    sync_fields = ['href', 'text', 'open_in_new_window']

    href = models.URLField(null=True, blank=True)
    text = models.CharField(max_length=2048, null=True, blank=True)
    open_in_new_window = models.BooleanField(default=True)
    sync_id = models.ForeignKey('URL', blank=True, null=True, on_delete=models.SET_NULL)


class SimpleList(Widget):
    type = 'simple_list'
    sync_fields = ['items', 'inner_border']

    items = models.JSONField(default=list)
    inner_border = models.BooleanField(default=True, help_text='Set border for items in list')
    sync_id = models.ForeignKey('SimpleList', blank=True, null=True, on_delete=models.SET_NULL)


class Counter(Widget):
    type = 'counter'
    sync_fields = ['value', 'vertical', 'step']

    value = models.BigIntegerField(default=0)
    vertical = models.BooleanField(default=True)
    step = models.IntegerField(default=1)
    sync_id = models.ForeignKey('Counter', blank=True, null=True, on_delete=models.SET_NULL)


class SimpleSwitch(Widget):
    type = 'simple_switch'
    sync_fields = ['value']

    value = models.BooleanField(default=False)
    sync_id = models.ForeignKey('SimpleSwitch', blank=True, null=True, on_delete=models.SET_NULL)


class Port(SyncManager):
    """ Describe static link ready to be distributed - link format should not change """
    type = 'port'

    title = models.CharField(max_length=200, blank=True, default='Untitled')
    wall = models.ForeignKey(Wall, on_delete=models.SET_NULL, null=True)
    visited = models.IntegerField(default=0, help_text='Visit counter')

    redirect_url = models.URLField(verbose_name='Redirect URL', help_text='Override default redirect (to this wall)',
                                   null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.propagate_instance_updated()

    def delete(self, *args, **kwargs):
        self.propagate_instance_deleted()
        super().delete(*args, **kwargs)
