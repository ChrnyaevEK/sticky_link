from application.data.abstract import BaseFactory
from django.db.models import Q


class ConcreteFactory(BaseFactory):

    @classmethod
    def _get_base_class(cls, base):
        class Base(base):
            related_wall_path = None
            related_owner_path = None

            owner_permission = False
            trusted_permission = False
            anonymous_permission = False

            @property
            def related_wall_instance(self):
                return None

            @property
            def related_owner_instance(self):
                return None

            @classmethod
            def build_trusted_query(cls, user):
                q = cls.related_wall_path + 'trusted_users__in' if cls.related_wall_path is not None else 'trusted_users__in'
                return Q(**{q: [user]})

            @classmethod
            def build_owned_query(cls, user):
                q = cls.related_wall_path + 'owner' if cls.related_wall_path is not None else 'owner'
                return Q(**{q: user})

            @classmethod
            def build_anonymous_query(cls, user):
                q = cls.related_wall_path + 'allow_anonymous_view' if cls.related_wall_path is not None else 'allow_anonymous_view'
                return Q(**{q: True})

            def set_permission(self, user):
                if not user.is_anonymous:
                    q = self.build_trusted_query(user)
                    self.trusted_permission = self.__class__.objects.filter(q).filter(pk=self.id).exists()

                    q = self.build_owned_query(user)
                    self.owner_permission = self.__class__.objects.filter(q).filter(pk=self.id).exists()

                q = self.build_anonymous_query(user)
                self.anonymous_permission = self.__class__.objects.filter(q).filter(pk=self.id).exists()

            class Meta:
                abstract = True

        return Base

    @classmethod
    def _get_widget_class(cls, base):
        class Widget(cls._get_base_class(base)):
            related_wall_path = 'container__wall__'
            related_owner_path = 'container__wall__owner__'

            @property
            def related_wall_instance(self):
                return self.container.related_wall_instance

            @property
            def related_owner_instance(self):
                return self.container.related_owner_instance

        return Widget

    @classmethod
    def get_wall_class(cls, base):
        class Wall(cls._get_base_class(base)):
            related_wall_path = ''
            related_owner_path = 'owner__'

            @property
            def related_wall_instance(self):
                return self

            @property
            def related_owner_instance(self):
                return self.owner

        return Wall

    @classmethod
    def get_container_class(cls, base):
        class Container(cls._get_base_class(base)):
            related_wall_path = 'wall__'
            related_owner_path = 'wall__owner__'

            @property
            def related_wall_instance(self):
                return self.wall.related_wall_instance

            @property
            def related_owner_instance(self):
                return self.wall.related_owner_instance

        return Container

    @classmethod
    def get_port_class(cls, base):
        class Port(cls._get_base_class(base)):
            related_owner_path = 'owner__'

            @property
            def related_owner_instance(self):
                return self.owner

            @classmethod
            def build_trusted_query(cls, user):
                return Q(owner=user, activated=True)

            @classmethod
            def build_owned_query(cls, user):
                return Q(owner=user, activated=True)

            @classmethod
            def build_anonymous_query(cls, user):
                return Q()  # All

        return Port

    @classmethod
    def get_source_class(cls, base):
        class Source(cls._get_base_class(base)):

            @property
            def related_wall_instance(self):
                return self.document_set.first().related_wall_instance

            @property
            def related_owner_instance(self):
                return self.document_set.first().related_owner_instance

        return Source

    @classmethod
    def get_simple_text_class(cls, base):
        return cls._get_widget_class(base)

    @classmethod
    def get_url_class(cls, base):
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
