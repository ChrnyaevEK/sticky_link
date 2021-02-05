"""
    Wall is a collection of Widgets. Each Widget has it's table and API.
    Walls are located in a different table and Wall id is a primary key for Widgets.
    Relay on ID's given by default
"""
from django.db import models
from django.core.validators import BaseValidator


class Settings:
    colors = [
        ['primary', 'Primary'],
        ['secondary', 'Secondary'],
        ['success', 'Success'],
        ['danger', 'Danger'],
        ['warning', 'Warning'],
        ['info', 'Info'],
        ['white', 'White'],
        ['black', 'Black'],
    ]
    default_background_color = 'white'
    default_text_color = 'black'
    default_z_index = 0
    default_widget_width = 200
    default_widget_height = 100


class Common(models.Model):
    id = models.AutoField(primary_key=True)
    date_of_creation = models.DateTimeField(verbose_name='Date of creation', auto_now_add=True)
    last_update = models.DateTimeField(verbose_name='Date of last update (wall or any widget)', auto_now=True)

    def __str__(self):
        return f'{type(self).__name__}: {self.id}'

    class Meta:
        abstract = True


class Wall(Common):
    type = 'wall'
    title = models.CharField(verbose_name='Wall title', max_length=200)
    description = models.CharField(verbose_name='Wall description', max_length=500, blank=True, null=True)


class Widget(Common):
    wall = models.ForeignKey(Wall, on_delete=models.CASCADE)
    width = models.IntegerField(verbose_name='Widget width', default=Settings.default_widget_width)
    height = models.IntegerField(verbose_name='Widget height', default=Settings.default_widget_height)
    z_index = models.IntegerField(verbose_name='Widget z index(stack position)', default=Settings.default_z_index)
    left = models.IntegerField(verbose_name='Offset left from parent', default=0)
    top = models.IntegerField(verbose_name='Offset top from parent', default=0)

    # TODO - html color
    background_color = models.CharField(max_length=10, choices=Settings.colors,
                                        default=Settings.default_background_color)
    text_color = models.CharField(max_length=10, choices=Settings.colors, default=Settings.default_text_color)

    class Meta:
        abstract = True


class SimpleText(Widget):
    type = 'simple_text'
    max_length = 2000
    text_content = models.TextField(verbose_name='Text content of widget', max_length=max_length, null=True, blank=True)


class RichText(Widget):
    type = 'rich_text'
    text_color = None  # Color is set by markdown
    text_content = models.TextField(verbose_name='Text content of widget', null=True, blank=True)
    show_source = models.BooleanField(default=True)


class URL(Widget):
    type = 'url'
    href = models.URLField(null=True, blank=True)


class SimpleListValidator(BaseValidator):
    max_items_amount = 20
    max_item_length = 100

    def compare(self, a, b):
        # Check type, items amount and length of each item
        isinstance(a, list) and len(a) <= self.max_items_amount and all([len(i) <= self.max_item_length for i in a])


class SimpleList(Widget):
    type = 'simple_list'
    max_title_length = 100
    max_description_length = 200
    title = models.CharField(max_length=max_title_length)
    description = models.CharField(max_length=max_description_length)
    items = models.JSONField(default=list, validators=[SimpleListValidator(None)])
