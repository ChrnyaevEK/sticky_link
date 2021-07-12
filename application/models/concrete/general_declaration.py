import re
import hashlib
import os.path

from django.db import models
from django.contrib.auth.models import User, AnonymousUser
from django.core.validators import BaseValidator, MaxValueValidator, MinValueValidator

from hashid_field import HashidAutoField

from application.models.abstract import BaseFactory

User.type = 'user'
AnonymousUser.username = 'anonymous'


class ColorValidator(BaseValidator):
    regex = re.compile(r'^#[0-9a-fA-F]{8}$|#[0-9a-fA-F]{6}$|#[0-9a-fA-F]{4}$|#[0-9a-fA-F]{3}$')  # ARGB hex color

    def compare(self, a, b):
        return self.regex.match(a)


def _to_hash(sting):
    return hashlib.md5(sting.encode('utf-8')).hexdigest()


class ConcreteFactory(BaseFactory):

    @classmethod
    def get_wall_class(cls, base):
        class Wall(cls._get_base_class(base)):
            owner = models.ForeignKey(User, on_delete=models.CASCADE)
            allow_anonymous_view = models.BooleanField(default=False)
            trusted_users = models.ManyToManyField(User, related_name='trusted_walls', blank=True)

            title = models.CharField(max_length=200, default='Untitled', null=True, blank=True)
            description = models.CharField(max_length=500, blank=True, null=True)
            lock_widgets = models.BooleanField(default=True)

            class Meta:
                abstract = True

        return Wall

    @classmethod
    def get_container_class(cls, base):
        class Container(cls._get_base_class(base)):
            wall = models.ForeignKey('Wall', on_delete=models.CASCADE)

            h = models.IntegerField(default=100, validators=[MinValueValidator(50)])
            w = models.IntegerField(default=3000)  # Should not change (is static)

            grid = models.BooleanField(default=False)

            title = models.CharField(max_length=200, null=True, blank=True)
            description = models.CharField(max_length=500, blank=True, null=True)

            class Meta:
                abstract = True

        return Container

    @classmethod
    def get_port_class(cls, base):
        class Port(cls._get_base_class(base)):
            activated = models.BooleanField(default=True)  # Internal use only

            title = models.CharField(max_length=200, blank=True, default='Untitled')
            owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
            visited = models.IntegerField(default=0, blank=True)
            authenticated_wall = models.ForeignKey('Wall', null=True, blank=True, on_delete=models.SET_NULL,
                                                   default=None, related_name='authenticated_wall')
            anonymous_wall = models.ForeignKey('Wall', null=True, blank=True, on_delete=models.SET_NULL, default=None,
                                               related_name='anonymous_wall')
            redirect_url = models.URLField(null=True, default=None, blank=True, max_length=2048)

            class Meta:
                abstract = True

        return Port

    @classmethod
    def get_source_class(cls, base):
        class Source(cls._get_base_class(base)):
            file = models.FileField(upload_to='%Y/%m/%d/', null=True)

            @property
            def name(self):
                try:
                    return os.path.basename(self.file.path)
                except ValueError:
                    return None

            class Meta:
                abstract = True

        return Source

    @classmethod
    def _get_widget_class(cls, base):
        class Widget(cls._get_base_class(base)):
            title = models.CharField(max_length=200, blank=True, null=True)
            description = models.CharField(max_length=500, blank=True, null=True)

            help = models.CharField(max_length=200, null=True, blank=True)

            w = models.IntegerField(default=200, validators=[MinValueValidator(50)])
            h = models.IntegerField(default=100, validators=[MinValueValidator(50)])
            z = models.IntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0)])
            x = models.IntegerField(default=0, validators=[MinValueValidator(0)])
            y = models.IntegerField(default=0, validators=[MinValueValidator(0)])

            font_size = models.IntegerField(default=14, validators=[MaxValueValidator(40), MinValueValidator(6)])
            font_weight = models.IntegerField(default=400,
                                              validators=[MaxValueValidator(900), MinValueValidator(100)])

            background_color = models.CharField(max_length=9, validators=[ColorValidator], default='#ffffff')
            text_color = models.CharField(max_length=9, validators=[ColorValidator], default='#000000')

            border = models.BooleanField(default=True)

            container = models.ForeignKey('Container', on_delete=models.CASCADE)

            class Meta:
                abstract = True

        return Widget

    @classmethod
    def _get_base_class(cls, base):
        class Base(base):
            type = None
            id = HashidAutoField(primary_key=True)

            date_of_creation = models.DateTimeField(auto_now_add=True)
            last_update = models.DateTimeField(auto_now=True)

            @property
            def uid(self):
                return _to_hash(f'{self.type}{self.id}')

            @property
            def version(self):
                return _to_hash(self.last_update.isoformat())

            @classmethod
            def exists(cls, pk):
                return cls.objects.filter(pk=pk).exists()

            class Meta:
                abstract = True

        return Base

    @classmethod
    def get_simple_text_class(cls, base):
        class SimpleText(cls._get_widget_class(base)):
            text_content = models.TextField(null=True, blank=True)

            class Meta:
                abstract = True

        return SimpleText

    @classmethod
    def get_url_class(cls, base):
        class URL(cls._get_widget_class(base)):
            href = models.URLField(null=True, blank=True, max_length=2048)
            open_in_new_window = models.BooleanField(default=True)

            class Meta:
                abstract = True

        return URL

    @classmethod
    def get_image_class(cls, base):
        class Image(cls._get_widget_class(base)):
            source = models.ForeignKey('Source', blank=True, on_delete=models.SET_NULL, null=True)
            alt = models.CharField(max_length=200, default='image', blank=True, null=True)

            class Meta:
                abstract = True

        return Image

    @classmethod
    def get_video_class(cls, base):
        class Video(cls._get_widget_class(base)):
            source = models.URLField(null=True, blank=True, max_length=2048)
            autoplay = models.BooleanField(default=False, blank=True)
            loop = models.BooleanField(default=False, blank=True)
            youtube = models.BooleanField(default=False, blank=True)

            class Meta:
                abstract = True

        return Video

    @classmethod
    def get_simple_list_class(cls, base):
        class SimpleList(cls._get_widget_class(base)):
            items = models.JSONField(default=list)
            inner_border = models.BooleanField(default=True)

            class Meta:
                abstract = True

        return SimpleList

    @classmethod
    def get_counter_class(cls, base):
        class Counter(cls._get_widget_class(base)):
            value = models.BigIntegerField(default=0)
            vertical = models.BooleanField(default=True)
            step = models.IntegerField(default=1)

            class Meta:
                abstract = True

        return Counter

    @classmethod
    def get_simple_switch_class(cls, base):
        class SimpleSwitch(cls._get_widget_class(base)):
            value = models.BooleanField(default=False)

            class Meta:
                abstract = True

        return SimpleSwitch

    @classmethod
    def get_document_class(cls, base):
        class Document(cls._get_widget_class(base)):
            # When copy widget - refer the same file (do not copy real file)
            source = models.ForeignKey('Source', blank=True, on_delete=models.SET_NULL, null=True)

            class Meta:
                abstract = True

        return Document
