from django.db import models


class Common(models.Model):
    class Meta:
        abstract = True


class Widget(models.Model):
    class Meta:
        abstract = True


class Wall(Common):
    class Meta:
        abstract = True


class Container(Common):
    class Meta:
        abstract = True


class Port(Common):
    class Meta:
        abstract = True


class Source(Common):
    class Meta:
        abstract = True


class SimpleText(Widget):
    class Meta:
        abstract = True


class URL(Widget):
    class Meta:
        abstract = True


class SimpleList(Widget):
    class Meta:
        abstract = True


class Counter(Widget):
    class Meta:
        abstract = True


class SimpleSwitch(Widget):
    class Meta:
        abstract = True


class Document(Widget):
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
        raise NotImplementedError()

    @classmethod
    def get_container_class(cls, base):
        raise NotImplementedError()

    @classmethod
    def get_port_class(cls, base):
        raise NotImplementedError()

    @classmethod
    def get_source_class(cls, base):
        raise NotImplementedError()

    @classmethod
    def get_simple_text_class(cls, base):
        raise NotImplementedError()

    @classmethod
    def get_url_class(cls, base):
        raise NotImplementedError()

    @classmethod
    def get_simple_list_class(cls, base):
        raise NotImplementedError()

    @classmethod
    def get_counter_class(cls, base):
        raise NotImplementedError()

    @classmethod
    def get_simple_switch_class(cls, base):
        raise NotImplementedError()

    @classmethod
    def get_document_class(cls, base):
        raise NotImplementedError()
