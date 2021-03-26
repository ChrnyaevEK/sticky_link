"""
    Wall is a collection of Widgets. Each Widget has it's table and API.
    Walls are located in a different table and Wall id is a primary key for Widgets.
    Relay on ID's given by default
"""
from django.db import models
from django.core.validators import BaseValidator, MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
import re
import hashlib


class Common(models.Model):
    type = None
    id = models.AutoField(primary_key=True)
    date_of_creation = models.DateTimeField(verbose_name='Date of creation', auto_now_add=True)
    last_update = models.DateTimeField(verbose_name='Date of last update (wall or any widget)', auto_now=True)

    def uid(self):
        return hashlib.md5(f'{self.type}{self.id}'.encode('utf-8')).hexdigest()

    def __str__(self):
        return f'{type(self).__name__}: {self.id}'

    class Meta:
        abstract = True


class Wall(Common):
    class Default:
        type = 'wall'
        title = 'Untitled'
        title_length = 200
        description_length = 500
        height = 600
        min_height = 100
        allow_anonymous_view = False
        lock_widgets = False
        protected_fields = [
            'id', 'uid', 'type', 'date_of_creation', 'last_update',
            'owner', 'allowed_users', 'allow_anonymous_view', 'title', 'description', 'lock_widgets',
            'w', 'h',
        ]

    type = Default.type
    h = models.IntegerField(verbose_name='Wall height', default=Default.height)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    allowed_users = models.ManyToManyField(User, verbose_name='List of allowed users',
                                           related_name='related_walls', blank=True)
    allow_anonymous_view = models.BooleanField('Allow anonymous view mode', default=Default.allow_anonymous_view)
    title = models.CharField(verbose_name='Wall title', max_length=Default.title_length, default=Default.title,
                             null=True, blank=True)
    description = models.CharField(verbose_name='Wall description', max_length=Default.description_length,
                                   blank=True, null=True)
    lock_widgets = models.BooleanField(verbose_name='Lock widgets custom actions', default=Default.lock_widgets)


class ColorValidator(BaseValidator):
    regex = re.compile(r'^#[0-9a-fA-F]{8}$|#[0-9a-fA-F]{6}$|#[0-9a-fA-F]{4}$|#[0-9a-fA-F]{3}$')  # ARGB hex color

    def compare(self, a, b):
        return self.regex.match(a)


# TODO - help_text
class Widget(Common):
    class Default:
        background_color = '#ffffff'
        text_color = '#000000'
        z = 0
        min_z = 0
        min_x = 0
        min_y = 0
        max_z = 1000
        font_size = 16
        min_font_size = 8
        max_font_size = 40
        font_weight = 400
        min_font_weight = 100
        max_font_weight = 900
        min_width = 50
        width = 200
        min_height = 50
        height = 150
        border = True
        help_length = 200
        protected_fields = [
            'id', 'uid', 'wall', 'type', 'date_of_creation', 'last_update',
            'font_size', 'font_weight', 'background_color', 'text_color', 'border', 'help',
            'w', 'h', 'z', 'x', 'y',
        ]

    wall = models.ForeignKey(Wall, on_delete=models.CASCADE)
    w = models.IntegerField(verbose_name='Widget width', default=Default.width)
    h = models.IntegerField(verbose_name='Widget height', default=Default.height)
    z = models.IntegerField(verbose_name='Widget z index(stack position)', default=Default.z, validators=[
        MaxValueValidator(Default.max_z), MinValueValidator(Default.min_z)
    ])
    x = models.IntegerField(verbose_name='Offset left from parent', default=Default.min_x, validators=[
        MinValueValidator(Default.min_x)
    ])
    y = models.IntegerField(verbose_name='Offset top from parent', default=Default.min_y, validators=[
        MinValueValidator(Default.min_y)
    ])
    font_size = models.IntegerField(verbose_name='Widget font size', default=Default.font_size,
                                    validators=[MaxValueValidator(Default.max_font_size),
                                                MinValueValidator(Default.min_font_size)])
    font_weight = models.IntegerField(verbose_name='Widget font weight', default=Default.font_weight,
                                      validators=[MaxValueValidator(Default.max_font_weight),
                                                  MinValueValidator(Default.min_font_weight)])

    background_color = models.CharField(max_length=9, validators=[ColorValidator], default=Default.background_color)
    text_color = models.CharField(max_length=9, validators=[ColorValidator], default=Default.text_color)
    border = models.BooleanField(default=Default.border)
    help = models.CharField(max_length=Default.help_length, null=True, blank=True)

    class Meta:
        abstract = True


class SimpleText(Widget):
    class Default:
        type = 'simple_text'

    type = Default.type
    text_content = models.TextField(verbose_name='Text content of widget', null=True,
                                    blank=True)


class URL(Widget):
    class Default:
        type = 'url'
        url_length = 2048

    type = Default.type
    href = models.URLField(null=True, blank=True)
    text = models.CharField(max_length=Default.url_length, null=True, blank=True)


class SimpleListValidator(BaseValidator):

    def compare(self, a, b):
        # Check type, items amount and length of each item
        isinstance(a, list) and all([len(i) <= SimpleList.Default.item_length for i in a])


class SimpleList(Widget):
    class Default:
        type = 'simple_list'
        item_length = 200
        title_length = 100
        description_length = 200

    type = Default.type
    title = models.CharField(max_length=Default.title_length, null=True, blank=True)
    description = models.CharField(max_length=Default.description_length, null=True, blank=True)
    items = models.JSONField(default=list, validators=[SimpleListValidator(None)])


class Counter(Widget):
    class Default:
        type = 'counter'
        title_length = 200
        initial_value = 0

    type = Default.type
    title = models.CharField(max_length=Default.title_length, blank=True, null=True)
    value = models.BigIntegerField(default=Default.initial_value)


class SimpleSwitch(Widget):
    class Default:
        type = 'simple_switch'
        title_length = 200
        initial_value = False

    type = Default.type
    title = models.CharField(max_length=Default.title_length, blank=True, null=True)
    value = models.BooleanField(default=Default.initial_value)


class Settings:
    widget = Widget.Default
    wall = Wall.Default
    simple_text = SimpleText.Default
    url = URL.Default
    simple_list = SimpleList.Default
    counter = Counter.Default
    simple_switch = SimpleSwitch.Default
