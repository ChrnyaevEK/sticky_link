from application.models.abstract import BaseFactory


class ConcreteFactory(BaseFactory):

    @classmethod
    def get_wall_class(cls, base):
        class Wall(base):
            type = 'wall'

            class Meta:
                abstract = True

        return Wall

    @classmethod
    def get_container_class(cls, base):
        class Container(base):
            type = 'container'

            class Meta:
                abstract = True

        return Container

    @classmethod
    def get_port_class(cls, base):
        class Port(base):
            type = 'port'

            class Meta:
                abstract = True

        return Port

    @classmethod
    def get_source_class(cls, base):
        class Source(base):
            type = 'source'

            class Meta:
                abstract = True

        return Source

    @classmethod
    def get_simple_text_class(cls, base):
        class SimpleText(base):
            type = 'simple_text'

            class Meta:
                abstract = True

        return SimpleText

    @classmethod
    def get_url_class(cls, base):
        class URL(base):
            type = 'url'

            class Meta:
                abstract = True

        return URL

    @classmethod
    def get_image_class(cls, base):
        class Image(base):
            type = 'image'

            class Meta:
                abstract = True

        return Image

    @classmethod
    def get_video_class(cls, base):
        class Video(base):
            type = 'video'

            class Meta:
                abstract = True

        return Video

    @classmethod
    def get_simple_list_class(cls, base):
        class SimpleList(base):
            type = 'simple_list'

            class Meta:
                abstract = True

        return SimpleList

    @classmethod
    def get_counter_class(cls, base):
        class Counter(base):
            type = 'counter'

            class Meta:
                abstract = True

        return Counter

    @classmethod
    def get_simple_switch_class(cls, base):
        class SimpleSwitch(base):
            type = 'simple_switch'

            class Meta:
                abstract = True

        return SimpleSwitch

    @classmethod
    def get_document_class(cls, base):
        class Document(base):
            type = 'document'

            class Meta:
                abstract = True

        return Document
