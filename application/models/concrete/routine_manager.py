from application.models.abstract import BaseFactory
from django.apps import apps
import os


class ConcreteFactory(BaseFactory):

    @classmethod
    def _get_widget_class(cls, base):
        class Widget(base):
            def save(self, *args, **kwargs):
                super().save(*args, **kwargs)
                self.propagate_instance_updated()
                self.synchronize_bounded_instances()

            def delete(self, *args, **kwargs):
                self.propagate_instance_deleted()
                for widget in self.__class__.objects.filter(sync_id=self):
                    widget.propagate_instance_updated()
                super().delete(*args, **kwargs)

            class Meta:
                abstract = True

        return Widget

    @classmethod
    def get_wall_class(cls, base):
        class Wall(base):
            def save(self, *args, **kwargs):
                super().save(*args, **kwargs)
                self.propagate_instance_updated()

            def delete(self, *args, **kwargs):
                self.propagate_instance_deleted()
                super().delete(*args, **kwargs)

            def initiate_default_container(self):
                container = apps.get_model(app_label='application', model_name='Container')(wall=self)
                container.save()
                return container

            class Meta:
                abstract = True

        return Wall

    @classmethod
    def get_container_class(cls, base):
        class Container(base):
            def save(self, *args, **kwargs):
                super().save(*args, **kwargs)
                self.propagate_instance_updated()

            def delete(self, *args, **kwargs):
                self.propagate_instance_deleted()
                super().delete(*args, **kwargs)

            class Meta:
                abstract = True

        return Container

    @classmethod
    def get_port_class(cls, base):
        class Port(base):
            def save(self, *args, **kwargs):
                super().save(*args, **kwargs)
                self.propagate_instance_updated()

            def delete(self, *args, **kwargs):
                self.propagate_instance_deleted()
                super().delete(*args, **kwargs)

            def resolve_target_wall(self, user):
                if user.is_authenticated and self.authenticated_wall:
                    if self.authenticated_wall.owner == user or user in self.authenticated_wall.trusted_users.all():
                        return self.authenticated_wall
                else:
                    return self.anonymous_wall

            def activate(self, user):
                self.activated = True
                self.owner = user

            class Meta:
                abstract = True

        return Port

    @classmethod
    def get_source_class(cls, base):
        class Source(base):
            def delete_file(self):
                try:
                    os.remove(self.file.path)
                except (ValueError, TypeError, OSError):
                    pass
                self.file = None
                self.save()

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
        class Image(cls._get_widget_class(base)):
            def delete(self, *args, **kwargs):
                if not self.exists(self.sync_id) and len(self.source.image_set.all()) == 1:
                    self.source.delete_file()
                    try:
                        self.source.delete()
                    except AttributeError:
                        pass  # Source has been deleted
                self.propagate_instance_deleted()
                super().delete(*args, **kwargs)

            class Meta:
                abstract = True

        return Image

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
        class Document(cls._get_widget_class(base)):
            def delete(self, *args, **kwargs):
                if not self.exists(self.sync_id) and len(self.source.document_set.all()) == 1:
                    self.source.delete_file()
                    try:
                        self.source.delete()
                    except AttributeError:
                        pass  # Source has been deleted
                self.propagate_instance_deleted()
                super().delete(*args, **kwargs)

            class Meta:
                abstract = True

        return Document
