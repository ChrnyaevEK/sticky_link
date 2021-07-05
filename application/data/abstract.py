from django.db import models


class Common(models.Model):
    class Meta:
        abstract = True


class Widget(models.Model):
    class Meta:
        abstract = True


class Wall(Common):
    pass


class Container(Common):
    pass


class Port(Common):
    pass


class Source(Common):
    pass


class SimpleText(Widget):
    pass


class URL(Widget):
    pass


class SimpleList(Widget):
    pass


class Counter(Widget):
    pass


class SimpleSwitch(Widget):
    pass


class Document(Widget):
    pass


class BaseFactory:
    @classmethod
    def get(cls, base):
        if isinstance(base, Wall):
            return cls.get_wall_class(base)
        if isinstance(base, Container):
            return cls.get_container_class(base)
        if isinstance(base, Port):
            return cls.get_port_class(base)
        if isinstance(base, Source):
            return cls.get_source_class(base)
        if isinstance(base, SimpleText):
            return cls.get_simple_text_class(base)
        if isinstance(base, URL):
            return cls.get_url_class(base)
        if isinstance(base, SimpleList):
            return cls.get_simple_list_class(base)
        if isinstance(base, SimpleSwitch):
            return cls.get_simple_switch_class(base)
        if isinstance(base, Counter):
            return cls.get_counter_class(base)
        if isinstance(base, Document):
            return cls.get_document_class(base)
        raise NotImplemented(f'Error! {base.__class__.__name__} has no declaration at {cls.__name__} factory')

    @classmethod
    def get_wall_class(cls, base):
        raise NotImplemented()

    @classmethod
    def get_container_class(cls, base):
        raise NotImplemented()

    @classmethod
    def get_port_class(cls, base):
        raise NotImplemented()

    @classmethod
    def get_source_class(cls, base):
        raise NotImplemented()

    @classmethod
    def get_simple_text_class(cls, base):
        raise NotImplemented()

    @classmethod
    def get_url_class(cls, base):
        raise NotImplemented()

    @classmethod
    def get_simple_list_class(cls, base):
        raise NotImplemented()

    @classmethod
    def get_counter_class(cls, base):
        raise NotImplemented()

    @classmethod
    def get_simple_switch_class(cls, base):
        raise NotImplemented()

    @classmethod
    def get_document_class(cls, base):
        raise NotImplemented()
