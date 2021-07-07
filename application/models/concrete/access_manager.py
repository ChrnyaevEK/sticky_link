from application.models.abstract import BaseFactory
from django.db.models import Q


class ConcreteFactory(BaseFactory):
    base_protected_fields = {'id', 'uid', 'version', 'type', 'date_of_creation', 'last_update'}

    @classmethod
    def _get_base_class(cls, base):
        class Base(base):
            related_wall_path = None
            related_owner_path = None

            protected_fields = cls.base_protected_fields

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

            @classmethod
            def get_owned(cls, user):
                if user.is_anonymous:
                    return cls.objects.none()
                q = cls.build_owned_query(user)
                return cls.objects.filter(q)

            @classmethod
            def get_trusted(cls, user):
                if user.is_anonymous:
                    return cls.objects.none()
                q = cls.build_trusted_query(user)
                return cls.objects.filter(q)

            @classmethod
            def get_anonymous(cls, user):
                q = cls.build_anonymous_query(user)
                return cls.objects.filter(q)

            @classmethod
            def get_reachable(cls, user):
                q = cls.build_anonymous_query(user)
                if not user.is_anonymous:
                    q.add(cls.build_trusted_query(user), q.OR)
                    q.add(cls.build_owned_query(user), q.OR)
                return cls.objects.filter(q).distinct()

            @classmethod
            def get_editable(cls, user):
                if user.is_anonymous:
                    return cls.objects.none()
                q = cls.build_trusted_query(user)
                q.add(cls.build_owned_query(user), q.OR)
                return cls.objects.filter(q).distinct()

            @classmethod
            def validate_anonymous_access(cls, accessed_fields):
                return not cls.protected_fields.intersection(accessed_fields)

            class Meta:
                abstract = True

        return Base

    @classmethod
    def _get_widget_class(cls, base):
        class Widget(cls._get_base_class(base)):
            related_wall_path = 'container__wall__'
            related_owner_path = 'container__wall__owner__'

            protected_fields = {'font_size', 'font_weight', 'background_color', 'text_color', 'border', 'help', 'w',
                                'h', 'z', 'x', 'y', 'sync_fields', 'container', 'owner', *cls.base_protected_fields}

            @property
            def related_wall_instance(self):
                return self.container.related_wall_instance

            @property
            def related_owner_instance(self):
                return self.container.related_owner_instance

            class Meta:
                abstract = True

        return Widget

    @classmethod
    def get_wall_class(cls, base):
        class Wall(cls._get_base_class(base)):
            related_wall_path = ''
            related_owner_path = 'owner__'

            protected_fields = {'owner', 'allowed_users', 'allow_anonymous_view', 'title', 'description',
                                'lock_widgets', *cls.base_protected_fields}

            @property
            def related_wall_instance(self):
                return self

            @property
            def related_owner_instance(self):
                return self.owner

            class Meta:
                abstract = True

        return Wall

    @classmethod
    def get_container_class(cls, base):
        class Container(cls._get_base_class(base)):
            related_wall_path = 'wall__'
            related_owner_path = 'wall__owner__'

            protected_fields = {'wall', 'next', 'h', 'w', 'description', 'title', *cls.base_protected_fields}

            @property
            def related_wall_instance(self):
                return self.wall.related_wall_instance

            @property
            def related_owner_instance(self):
                return self.wall.related_owner_instance

            class Meta:
                abstract = True

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
                return Q()

            @classmethod
            def validate_anonymous_access(cls, accessed_fields):
                return False

            class Meta:
                abstract = True

        return Port

    @classmethod
    def get_source_class(cls, base):
        class Source(cls._get_base_class(base)):
            related_wall_path = 'document_set__container__wall__'
            related_owner_path = 'document_set__container__wall__owner__'

            @property
            def related_wall_instance(self):
                return self.document_set.first().related_wall_instance

            @property
            def related_owner_instance(self):
                return self.document_set.first().related_owner_instance

            @classmethod
            def validate_anonymous_access(cls, accessed_fields):
                return False

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
