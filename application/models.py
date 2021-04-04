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
    type = 'wall'
    protected_fields = [
        'id', 'uid', 'type', 'date_of_creation', 'last_update',
        'owner', 'allowed_users', 'allow_anonymous_view', 'title', 'description', 'lock_widgets',
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    allow_anonymous_view = models.BooleanField('Allow anonymous view mode', default=False)
    title = models.CharField(verbose_name='Wall title', max_length=200, default='Untitled', null=True, blank=True)
    description = models.CharField(verbose_name='Wall description', max_length=500, blank=True, null=True)
    lock_widgets = models.BooleanField(verbose_name='Lock widgets at wall', default=False)


class Container(Common):
    type = 'container'
    protected_fields = [
        'id', 'uid', 'type', 'date_of_creation', 'last_update',
        'wall', 'index', 'h', 'w', 'description', 'title',
    ]
    wall = models.ForeignKey(Wall, on_delete=models.CASCADE)
    index = models.IntegerField(verbose_name='Index of container in wall', validators=[MinValueValidator(0)])
    h = models.IntegerField(verbose_name='Container height', default=100, validators=[MinValueValidator(50)])
    w = models.IntegerField(verbose_name='Container width', default=2000)  # Should not change (is static)
    title = models.CharField(verbose_name='Container title', max_length=200, null=True, blank=True)
    description = models.CharField(verbose_name='Container description', max_length=500, blank=True, null=True)


class ColorValidator(BaseValidator):
    regex = re.compile(r'^#[0-9a-fA-F]{8}$|#[0-9a-fA-F]{6}$|#[0-9a-fA-F]{4}$|#[0-9a-fA-F]{3}$')  # ARGB hex color

    def compare(self, a, b):
        return self.regex.match(a)


class Widget(Common):
    protected_fields = [
        'id', 'uid', 'wall', 'type', 'date_of_creation', 'last_update',
        'font_size', 'font_weight', 'background_color', 'text_color', 'border', 'help',
        'w', 'h', 'z', 'x', 'y',
    ]
    container = models.ForeignKey(Container, on_delete=models.CASCADE)

    w = models.IntegerField(verbose_name='Widget width', default=200, validators=[MinValueValidator(50)])
    h = models.IntegerField(verbose_name='Widget height', default=130, validators=[MinValueValidator(50)])
    z = models.IntegerField(verbose_name='Widget z index(stack position)', default=0,
                            validators=[MaxValueValidator(100), MinValueValidator(0)])
    x = models.IntegerField(verbose_name='Offset left from parent', default=0, validators=[MinValueValidator(0)])
    y = models.IntegerField(verbose_name='Offset top from parent', default=0, validators=[MinValueValidator(0)])
    font_size = models.IntegerField(verbose_name='Widget font size', default=16,
                                    validators=[MaxValueValidator(40), MinValueValidator(6)])
    font_weight = models.IntegerField(verbose_name='Widget font weight', default=400,
                                      validators=[MaxValueValidator(900), MinValueValidator(100)])
    background_color = models.CharField(max_length=9, validators=[ColorValidator], default='#ffffff')
    text_color = models.CharField(max_length=9, validators=[ColorValidator], default='#000000')
    border = models.BooleanField(default=True)
    help = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        abstract = True


class SimpleText(Widget):
    type = 'simple_text'
    text_content = models.TextField(verbose_name='Text content of widget', null=True, blank=True)


class URL(Widget):
    type = 'url'
    href = models.URLField(null=True, blank=True)
    text = models.CharField(max_length=2048, null=True, blank=True)


class SimpleList(Widget):
    type = 'simple_list'
    title = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    items = models.JSONField(default=list)


class Counter(Widget):
    type = 'counter'
    title = models.CharField(max_length=200, blank=True, null=True)
    value = models.BigIntegerField(default=0)


class SimpleSwitch(Widget):
    type = 'simple_switch'
    title = models.CharField(max_length=200, blank=True, null=True)
    value = models.BooleanField(default=False)
