"""
    Wall is a collection of Widgets. Each Widget has it's table and API.
    Walls are located in a different table and Wall id is a primary key for Widgets.
    Relay on ID's given by default
"""
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Settings:
    colors = (
        ('primary', 'Primary'),
        ('secondary', 'Secondary'),
        ('success', 'Success'),
        ('danger', 'Danger'),
        ('warning', 'Warning'),
        ('info', 'Info'),
        ('white', 'White'),
        ('black', 'White'),
    )
    default_background_color = 'white'
    default_text_color = 'black'
    max_widget_width = 2000
    min_widget_width = 200
    max_widget_height = 2000
    min_widget_height = 100


class Common(models.Model):
    id = models.AutoField(primary_key=True)
    date_of_creation = models.DateTimeField(verbose_name='Date of creation', auto_now_add=True)
    last_update = models.DateTimeField(verbose_name='Date of last update (wall or any widget)', auto_now=True)

    def __str__(self):
        return f'{type(self).__name__}: {self.id}'

    class Meta:
        abstract = True


class Wall(Common):
    title = models.CharField(verbose_name='Wall title', max_length=200)
    description = models.CharField(verbose_name='Wall description', max_length=500, blank=True, null=True)


class Widget(Common):
    wall = models.ForeignKey(Wall, on_delete=models.CASCADE)
    width = models.IntegerField(verbose_name='Widget width', default=Settings.min_widget_width, validators=[
        MinValueValidator(Settings.min_widget_width), MaxValueValidator(Settings.max_widget_width)
    ])
    height = models.IntegerField(verbose_name='Widget height', default=Settings.min_widget_height, validators=[
        MinValueValidator(Settings.min_widget_height), MaxValueValidator(Settings.max_widget_height)
    ])
    left = models.IntegerField(verbose_name='Offset left from parent', default=0, validators=[MinValueValidator(0)])
    top = models.IntegerField(verbose_name='Offset top from parent', default=0, validators=[MinValueValidator(0)])

    class Meta:
        abstract = True


class SimpleText(Widget):
    max_length = 2000
    text_content = models.TextField(verbose_name='Text content of widget', max_length=max_length)
    font_color = models.CharField(max_length=10, choices=Settings.colors, default=Settings.default_text_color)
    background_color = models.CharField(max_length=10, choices=Settings.colors,
                                        default=Settings.default_background_color)
