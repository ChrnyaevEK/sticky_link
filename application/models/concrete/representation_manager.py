from application.models.abstract import BaseFactory


class ConcreteFactory(BaseFactory):
    @classmethod
    def _get_base_class(cls, base):
        class Base(base):
            def __str__(self):
                return f'{type(self).__name__}: {self.id}'

            class Meta:
                abstract = True

        return Base

    @classmethod
    def _get_widget_class(cls, base):
        class Widget(cls._get_base_class(base)):
            def __str__(self):
                return f'{self.id} | {self.title or "Untitled widget"}'

            class Meta:
                abstract = True

        return Widget

    @classmethod
    def get_wall_class(cls, base):
        class Wall(base):
            def __str__(self):
                return f'{self.id} | {self.title or "Untitled wall"}'

            class Meta:
                abstract = True

        return Wall

    @classmethod
    def get_container_class(cls, base):
        class Container(base):
            def __str__(self):
                return f'{self.id} | {self.title or "Untitled container"}'

            class Meta:
                abstract = True

        return Container

    @classmethod
    def get_port_class(cls, base):
        class Port(base):
            def __str__(self):
                return f'{self.id} | {self.title or "Untitled port"}'

            class Meta:
                abstract = True

        return Port

    @classmethod
    def get_source_class(cls, base):
        class Source(base):
            def __str__(self):
                return f'{self.id} | {self.name or "Untitled source"}'

            class Meta:
                abstract = True

        return Source

    @classmethod
    def get_simple_text_class(cls, base):
        return cls._get_widget_class(base)

    @classmethod
    def get_url_class(cls, base):
        return cls._get_widget_class(base)

    @classmethod
    def get_image_class(cls, base):
        return cls._get_widget_class(base)

    @classmethod
    def get_video_class(cls, base):
        return cls._get_widget_class(base)

    @classmethod
    def get_simple_list_class(cls, base):
        return cls._get_widget_class(base)

    @classmethod
    def get_counter_class(cls, base):
        return cls._get_widget_class(base)

    @classmethod
    def get_simple_switch_class(cls, base):
        return cls._get_widget_class(base)

    @classmethod
    def get_document_class(cls, base):
        return cls._get_widget_class(base)
