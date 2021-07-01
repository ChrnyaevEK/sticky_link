import os.path
import re
from django.db import models
from django.core.validators import BaseValidator, MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User, AnonymousUser
from hashid_field import HashidAutoField
from channels.layers import get_channel_layer
from application.consumers import Event as ConsumerEvent, WallConsumer
from asgiref.sync import async_to_sync
import hashlib
from django.db.models import Q

User.type = 'user'
AnonymousUser.username = 'anonymous'


def _to_hash(sting):
    return hashlib.md5(sting.encode('utf-8')).hexdigest()


class Protected(models.Model):
    owner_permission = False
    trusted_permission = False
    anonymous_permission = False

    _wall_path: str = None  # Path prefix to the wall instance (for permission check)
    _protected_fields = {'id', 'uid', 'version', 'type', 'date_of_creation', 'last_update'}

    class Meta:
        abstract = True

    @classmethod
    def build_trusted_query(cls, user):
        trusted_users = 'trusted_users__in'
        if cls._wall_path is not None:
            trusted_users = cls._wall_path + trusted_users

        return Q(**{trusted_users: [user]})

    @classmethod
    def build_owned_query(cls, user):
        owner = 'owner'
        if cls._wall_path is not None:
            owner = cls._wall_path + owner
        return Q(**{owner: user})

    @classmethod
    def build_anonymous_query(cls, user):
        anonymous = 'allow_anonymous_view'
        if cls._wall_path is not None:
            anonymous = cls._wall_path + anonymous
        return Q(**{anonymous: True})

    def set_permission(self, user):
        self._set_has_anonymous_permission(user)
        self._set_has_trusted_permission(user)
        self._set_has_owner_permission(user)

    def _set_has_owner_permission(self, user):
        if user.is_anonymous:
            return False
        q = self.build_owned_query(user)
        self.owner_permission = self.__class__.objects.filter(q).filter(pk=self.id).exists()

    def _set_has_trusted_permission(self, user):
        if user.is_anonymous:
            return False
        q = self.build_trusted_query(user)
        self.trusted_permission = self.__class__.objects.filter(q).filter(pk=self.id).exists()

    def _set_has_anonymous_permission(self, user):
        q = self.build_anonymous_query(user)
        self.anonymous_permission = self.__class__.objects.filter(q).filter(pk=self.id).exists()

    @classmethod
    def get_reachable(cls, user):
        q = cls.build_anonymous_query(user)
        if not user.is_anonymous:
            q.add(cls.build_trusted_query(user), q.OR)
            q.add(cls.build_owned_query(user), q.OR)
        return cls.objects.filter(q).distinct()

    @classmethod
    def validate_anonymous_access(cls, accessed_fields):
        return not cls._protected_fields.intersection(accessed_fields)


class Base(Protected):
    type = None
    id = HashidAutoField(primary_key=True)

    date_of_creation = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f'{type(self).__name__}: {self.id}'

    @property
    def related_wall_instance(self):
        try:
            return self.document_set.first().container.wall
        except AttributeError:
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

    def copy(self):
        clone = self.__class__.objects.get(pk=self.pk)
        clone.id = None
        clone.pk = None
        clone.save()
        return clone


class SyncManager(Base):
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

    @classmethod
    def has_any_sync_widget(cls, sync_id):
        return cls.objects.filter(pk=sync_id).exists()


class Wall(SyncManager):
    type = 'wall'

    _protected_fields = {'owner', 'allowed_users', 'allow_anonymous_view', 'title', 'description', 'lock_widgets'}
    _protected_fields.update(Base._protected_fields)

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    allow_anonymous_view = models.BooleanField(default=False)
    trusted_users = models.ManyToManyField(User, related_name='trusted_walls', blank=True)

    title = models.CharField(max_length=200, default='Untitled', null=True, blank=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    lock_widgets = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.id} | {self.title or "Untitled wall"}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.propagate_instance_updated()

    def delete(self, *args, **kwargs):
        self.propagate_instance_deleted()
        super().delete(*args, **kwargs)

    @classmethod
    def get_owned_walls(cls, user):
        if user.is_anonymous:
            return cls.objects.none()
        q = cls.build_owned_query(user)
        return cls.objects.filter(q)

    @classmethod
    def get_trusted_walls(cls, user):
        if user.is_anonymous:
            return cls.objects.none()
        q = cls.build_trusted_query(user)
        return cls.objects.filter(q)

    def initiate_default_container(self):
        container = Container(wall=self)
        container.save()
        return container

    def copy(self):
        clone = super().copy()
        for container in self.container_set.all():
            clone.container_set.add(container.copy())
        clone.save()
        return clone

    def chain_new_container(self, container):
        last = self.container_set.last()
        last.next = container
        last.save()

    def fix_container_chaining(self):
        previous = None
        start_list = []
        for container in self.container_set.order('date_of_creation').all():
            if container.wall != self:
                raise ValueError('Unexpected foreign container')
            # Chain all unchained containers
            if container.next is None and container.previous is None:
                if previous is not None:
                    previous.next = container
                    previous.save()
                previous = container
            # Collect chain starts
            if container.next is not None and container.previous is None:  # Chain start
                start_list.append(container)

        if len(start_list) == 1:  # Nothing to chain
            return

        def chain_container(cnt, arr):
            if cnt.next is None:
                return
            arr.append(cnt.next)
            chain_container(cnt.next, arr)

        chain_list = []
        for start in start_list:
            chain = [start]
            chain_container(start, chain)
            chain_list.append(chain)

        # Chain chains
        previous_chain = None
        for chain in chain_list:
            if previous_chain is not None:
                previous_chain[-1].next = chain[0]
                previous_chain[-1].save()
            previous_chain = chain


class Container(SyncManager):
    type = 'container'
    _wall_path = 'wall__'
    _protected_fields = {'wall', 'next', 'h', 'w', 'description', 'title'}
    _protected_fields.update(Base._protected_fields)

    wall = models.ForeignKey(Wall, on_delete=models.CASCADE)
    next = models.OneToOneField('Container', on_delete=models.SET_NULL, null=True, default=None, blank=True,
                                related_name='previous')

    h = models.IntegerField(default=100, validators=[MinValueValidator(50)])
    w = models.IntegerField(default=3000)  # Should not change (is static)
    grid = models.BooleanField(default=False)

    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f'{self.id} | {self.title or "Untitled container"}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.propagate_instance_updated()

    def _by_pass_next(self):
        try:
            self.previous.next = self.next
        except AttributeError:
            pass

    def delete(self, *args, **kwargs):
        self._by_pass_next()
        self.propagate_instance_deleted()
        super().delete(*args, **kwargs)

    def copy(self):
        clone = super().copy()
        for w in self.simple_text_set.all():
            clone.simple_text_set.add(w.copy())

        for w in self.url_set.all():
            clone.url_set.add(w.copy())

        for w in self.simple_list_set.all():
            clone.simple_list_set.add(w.copy())

        for w in self.counter_set.all():
            clone.counter_set.add(w.copy())

        for w in self.simple_switch_set.all():
            clone.simple_switch_set.add(w.copy())

        for w in self.document_set.all():
            clone.document_set.add(w.copy())
        clone.save()
        return clone


class Port(SyncManager):
    """ Describe static link ready to be distributed - link format should not change """
    type = 'port'

    activated = models.BooleanField(default=True)  # Internal use only

    title = models.CharField(max_length=200, blank=True, default='Untitled')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    visited = models.IntegerField(default=0)
    authenticated_wall = models.ForeignKey(Wall, null=True, blank=True, on_delete=models.SET_NULL, default=None,
                                           related_name='authenticated_wall')
    anonymous_wall = models.ForeignKey(Wall, null=True, blank=True, on_delete=models.SET_NULL, default=None,
                                       related_name='anonymous_wall')
    redirect_url = models.URLField(null=True, default=None, blank=True)

    def __str__(self):
        return f'{self.id} | {self.title or "Untitled port"}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.propagate_instance_updated()

    def delete(self, *args, **kwargs):
        self.propagate_instance_deleted()
        super().delete(*args, **kwargs)

    def resolve_target_wall(self, user):
        if user.is_authenticated and self.authenticated_wall:
            if self.authenticated_wall.owner == user or user in self.authenticated_wall.trusted_users.all():
                return self.authenticated_wall
        else:
            return self.anonymous_wall

    @classmethod
    def build_trusted_query(cls, user):
        return Q(owner=user, activated=True)

    @classmethod
    def build_owned_query(cls, user):
        return Q(owner=user, activated=True)

    @classmethod
    def build_anonymous_query(cls, user):
        return Q()  # All

    @classmethod
    def get_owned_ports(cls, user):
        if user.is_anonymous:
            return cls.objects.none()
        q = cls.build_owned_query(user)
        return cls.objects.filter(q)

    @classmethod
    def get_anonymous_ports(cls, user):
        q = cls.build_anonymous_query(user)
        return cls.objects.filter(q)

    def activate(self, user):
        self.activated = True
        self.owner = user


class Source(Base):
    _wall_path = 'document_set__container__wall__'
    file = models.FileField(upload_to='%Y/%m/%d/', null=True)

    @classmethod
    def validate_anonymous_access(cls, accessed_fields):
        return False

    @property
    def name(self):
        try:
            return os.path.basename(self.file.path)
        except ValueError:
            return None

    def delete_file(self):
        try:
            os.remove(self.file.path)
        except (ValueError, TypeError, OSError):
            pass
        self.save()

    def __str__(self):
        return f'{self.id} | {self.name or "Untitled source"}'


class ColorValidator(BaseValidator):
    regex = re.compile(r'^#[0-9a-fA-F]{8}$|#[0-9a-fA-F]{6}$|#[0-9a-fA-F]{4}$|#[0-9a-fA-F]{3}$')  # ARGB hex color

    def compare(self, a, b):
        return self.regex.match(a)


class Widget(SyncManager):
    _wall_path = 'container__wall__'
    _protected_fields = {'font_size', 'font_weight', 'background_color', 'text_color', 'border', 'help', 'w', 'h',
                         'z', 'x', 'y', 'sync_fields', 'container', 'owner'}
    _protected_fields.update(Base._protected_fields)
    title = models.CharField(max_length=200, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)

    help = models.CharField(max_length=200, null=True, blank=True)

    w = models.IntegerField(default=200, validators=[MinValueValidator(50)])
    h = models.IntegerField(default=100, validators=[MinValueValidator(50)])
    z = models.IntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0)])
    x = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    y = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    font_size = models.IntegerField(default=14, validators=[MaxValueValidator(40), MinValueValidator(6)])
    font_weight = models.IntegerField(default=400, validators=[MaxValueValidator(900), MinValueValidator(100)])

    background_color = models.CharField(max_length=9, validators=[ColorValidator], default='#ffffff')
    text_color = models.CharField(max_length=9, validators=[ColorValidator], default='#000000')

    border = models.BooleanField(default=True)

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

    def __str__(self):
        return f'{self.id} | {self.title or "Untitled widget"}'

    class Meta:
        abstract = True


class SimpleText(Widget):
    type = 'simple_text'
    sync_fields = ['text_content']
    sync_id = models.ForeignKey('SimpleText', blank=True, null=True, on_delete=models.SET_NULL)

    container = models.ForeignKey(Container, on_delete=models.CASCADE, related_name='simple_text_set')

    text_content = models.TextField(null=True, blank=True)


class URL(Widget):
    type = 'url'
    sync_fields = ['href', 'text', 'open_in_new_window']
    sync_id = models.ForeignKey('URL', blank=True, null=True, on_delete=models.SET_NULL)

    container = models.ForeignKey(Container, on_delete=models.CASCADE, related_name='url_set')

    href = models.URLField(null=True, blank=True)
    open_in_new_window = models.BooleanField(default=True)


class SimpleList(Widget):
    type = 'simple_list'
    sync_fields = ['items', 'inner_border']
    sync_id = models.ForeignKey('SimpleList', blank=True, null=True, on_delete=models.SET_NULL)

    container = models.ForeignKey(Container, on_delete=models.CASCADE, related_name='simple_list_set')

    items = models.JSONField(default=list)
    inner_border = models.BooleanField(default=True)


class Counter(Widget):
    type = 'counter'
    sync_fields = ['value', 'vertical', 'step']
    sync_id = models.ForeignKey('Counter', blank=True, null=True, on_delete=models.SET_NULL)

    container = models.ForeignKey(Container, on_delete=models.CASCADE, related_name='counter_set')

    value = models.BigIntegerField(default=0)
    vertical = models.BooleanField(default=True)
    step = models.IntegerField(default=1)


class SimpleSwitch(Widget):
    type = 'simple_switch'
    sync_fields = ['value']
    sync_id = models.ForeignKey('SimpleSwitch', blank=True, null=True, on_delete=models.SET_NULL)

    container = models.ForeignKey(Container, on_delete=models.CASCADE, related_name='simple_switch_set')

    value = models.BooleanField(default=False)


class Document(Widget):
    type = 'document'
    sync_fields = ['source']
    sync_id = models.ForeignKey('Document', blank=True, null=True, on_delete=models.SET_NULL)

    container = models.ForeignKey(Container, on_delete=models.CASCADE, related_name='document_set')

    # When copy widget - refer the same source (do not copy real file)
    source = models.ForeignKey(Source, blank=True, on_delete=models.SET_NULL, null=True, related_name='document_set')

    def delete(self, *args, **kwargs):
        if not self.has_any_sync_widget(self.sync_id) and len(self.source.document_set.all()) == 1:
            self.source.delete_file()
            try:
                self.source.delete()
            except AttributeError:
                pass  # Source has been deleted
        super().delete(*args, **kwargs)


class Meta:
    file_size_max = 10485760


class Permission:
    def __init__(self, instance, user):
        self.owner_permission = instance.has_owner_permission(user)
        self.trusted_permission = instance.has_trusted_permission(user)
        self.anonymous_permission = instance.has_anonymous_permission(user)
