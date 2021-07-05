from application.data.abstract import BaseFactory


class ConcreteFactory(BaseFactory):

    @staticmethod
    def get_wall_class(base):
        class Wall(base):
            type = 'wall'

        return Wall

    @staticmethod
    def get_container_class(base):
        class Container(base):
            type = 'container'

        return Container

    @staticmethod
    def get_port_class(base):
        class Port(base):
            type = 'port'

        return Port

    @staticmethod
    def get_source_class(base):
        class Source(base):
            type = 'source'

        return Source

    @staticmethod
    def get_simple_text_class(base):
        class SimpleText(base):
            type = 'simple_text'

        return SimpleText

    @staticmethod
    def get_url_class(base):
        class URL(base):
            type = 'url'

        return URL

    @staticmethod
    def get_simple_list_class(base):
        class SimpleList(base):
            type = 'simple_list'

        return SimpleList

    @staticmethod
    def get_counter_class(base):
        class Counter(base):
            type = 'counter'

        return Counter

    @staticmethod
    def get_simple_switch_class(base):
        class SimpleSwitch(base):
            type = 'simple_switch'

        return SimpleSwitch

    @staticmethod
    def get_document_class(base):
        class Document(base):
            type = 'document'

        return Document
