"""
    Wall is a collection of Widgets. Each Widget has it's table and API.
    Walls are located in a different table and Wall id is a primary key for Widgets.
    Relay on ID's given by default
"""
from django.db import models


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

    class Meta:
        abstract = True


class SimpleTextWidget(Widget):
    text_content = models.TextField(verbose_name='Text content of widget', max_length=2000)
