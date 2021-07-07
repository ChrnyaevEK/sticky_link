from django.db import models


class Wall(models.Model):
    class Meta:
        abstract = True


class Container(models.Model):
    class Meta:
        abstract = True


class Port(models.Model):
    class Meta:
        abstract = True


class Source(models.Model):
    class Meta:
        abstract = True


class SimpleText(models.Model):
    class Meta:
        abstract = True


class URL(models.Model):
    class Meta:
        abstract = True


class Image(models.Model):
    class Meta:
        abstract = True


class Video(models.Model):
    class Meta:
        abstract = True


class SimpleList(models.Model):
    class Meta:
        abstract = True


class Counter(models.Model):
    class Meta:
        abstract = True


class SimpleSwitch(models.Model):
    class Meta:
        abstract = True


class Document(models.Model):
    class Meta:
        abstract = True


class BaseFactory:
    @classmethod
    def get(cls, base):
        if issubclass(base, Wall):
            return cls.get_wall_class(base)
        if issubclass(base, Container):
            return cls.get_container_class(base)
        if issubclass(base, Port):
            return cls.get_port_class(base)
        if issubclass(base, Source):
            return cls.get_source_class(base)
        if issubclass(base, SimpleText):
            return cls.get_simple_text_class(base)
        if issubclass(base, URL):
            return cls.get_url_class(base)
        if issubclass(base, Image):
            return cls.get_image_class(base)
        if issubclass(base, Video):
            return cls.get_video_class(base)
        if issubclass(base, SimpleList):
            return cls.get_simple_list_class(base)
        if issubclass(base, SimpleSwitch):
            return cls.get_simple_switch_class(base)
        if issubclass(base, Counter):
            return cls.get_counter_class(base)
        if issubclass(base, Document):
            return cls.get_document_class(base)
        raise NotImplementedError(f'Error! {base} was not found at {cls}')

    @classmethod
    def get_wall_class(cls, base):
        return base

    @classmethod
    def get_container_class(cls, base):
        return base

    @classmethod
    def get_port_class(cls, base):
        return base

    @classmethod
    def get_source_class(cls, base):
        return base

    @classmethod
    def get_simple_text_class(cls, base):
        return base

    @classmethod
    def get_url_class(cls, base):
        return base

    @classmethod
    def get_image_class(cls, base):
        return base

    @classmethod
    def get_video_class(cls, base):
        return base

    @classmethod
    def get_simple_list_class(cls, base):
        return base

    @classmethod
    def get_counter_class(cls, base):
        return base

    @classmethod
    def get_simple_switch_class(cls, base):
        return base

    @classmethod
    def get_document_class(cls, base):
        return base
