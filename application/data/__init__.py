import os.path
import re
from django.db import models
from django.core.validators import BaseValidator, MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User, AnonymousUser
from hashid_field import HashidAutoField
import hashlib

User.type = 'user'
AnonymousUser.username = 'anonymous'


def _to_hash(sting):
    return hashlib.md5(sting.encode('utf-8')).hexdigest()


class Base(models.Model):
    type = None
    id = HashidAutoField(primary_key=True)

    date_of_creation = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{type(self).__name__}: {self.id}'

    @property
    def uid(self):
        return _to_hash(f'{self.type}{self.id}')

    @property
    def version(self):
        return _to_hash(self.last_update.isoformat())

    class Meta:
        abstract = True


class Wall(Base):
    type = 'wall'

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    allow_anonymous_view = models.BooleanField(default=False)
    trusted_users = models.ManyToManyField(User, related_name='trusted_walls', blank=True)

    title = models.CharField(max_length=200, default='Untitled', null=True, blank=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    lock_widgets = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.id} | {self.title or "Untitled"}'


class Container(Base):
    type = 'container'

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


class Port(Base):
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


class Source(Base):
    file = models.FileField(upload_to='%Y/%m/%d/', null=True)

    @property
    def name(self):
        try:
            return os.path.basename(self.file.path)
        except ValueError:
            return None

    def __str__(self):
        return f'{self.id} | {self.name or "Untitled source"}'


class ColorValidator(BaseValidator):
    regex = re.compile(r'^#[0-9a-fA-F]{8}$|#[0-9a-fA-F]{6}$|#[0-9a-fA-F]{4}$|#[0-9a-fA-F]{3}$')  # ARGB hex color

    def compare(self, a, b):
        return self.regex.match(a)


class Widget(Base):
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

    def __str__(self):
        return f'{self.id} | {self.title or "Untitled widget"}'

    class Meta:
        abstract = True


class SimpleText(Widget):
    type = 'simple_text'
    sync_id = models.ForeignKey('SimpleText', blank=True, null=True, on_delete=models.SET_NULL)

    container = models.ForeignKey(Container, on_delete=models.CASCADE, related_name='simple_text_set')

    text_content = models.TextField(null=True, blank=True)


class URL(Widget):
    type = 'url'
    sync_id = models.ForeignKey('URL', blank=True, null=True, on_delete=models.SET_NULL)

    container = models.ForeignKey(Container, on_delete=models.CASCADE, related_name='url_set')

    href = models.URLField(null=True, blank=True)
    open_in_new_window = models.BooleanField(default=True)


class SimpleList(Widget):
    type = 'simple_list'
    sync_id = models.ForeignKey('SimpleList', blank=True, null=True, on_delete=models.SET_NULL)

    container = models.ForeignKey(Container, on_delete=models.CASCADE, related_name='simple_list_set')

    items = models.JSONField(default=list)
    inner_border = models.BooleanField(default=True)


class Counter(Widget):
    type = 'counter'
    sync_id = models.ForeignKey('Counter', blank=True, null=True, on_delete=models.SET_NULL)

    container = models.ForeignKey(Container, on_delete=models.CASCADE, related_name='counter_set')

    value = models.BigIntegerField(default=0)
    vertical = models.BooleanField(default=True)
    step = models.IntegerField(default=1)


class SimpleSwitch(Widget):
    type = 'simple_switch'
    sync_id = models.ForeignKey('SimpleSwitch', blank=True, null=True, on_delete=models.SET_NULL)

    container = models.ForeignKey(Container, on_delete=models.CASCADE, related_name='simple_switch_set')

    value = models.BooleanField(default=False)


class Document(Widget):
    type = 'document'
    sync_id = models.ForeignKey('Document', blank=True, null=True, on_delete=models.SET_NULL)

    container = models.ForeignKey(Container, on_delete=models.CASCADE, related_name='document_set')

    # When copy widget - refer the same file (do not copy real file)
    source = models.ForeignKey(Source, blank=True, on_delete=models.SET_NULL, null=True, related_name='document_set')


class Meta:
    file_size_max = 10485760
