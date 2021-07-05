from application.models.abstract import BaseFactory


class ConcreteFactory(BaseFactory):

    @classmethod
    def _get_base_class(cls, base):
        class Base(base):
            def copy(self):
                clone = self.__class__.objects.get(pk=self.pk)
                clone.id = None
                clone.pk = None
                clone.save()
                return clone

            class Meta:
                abstract = True

        return Base

    @classmethod
    def get_wall_class(cls, base):
        class Wall(cls._get_base_class(base)):
            def copy(self):
                clone = super().copy()
                for container in self.container_set.all():
                    clone.container_set.add(container.copy())
                clone.save()
                return clone

            class Meta:
                abstract = True

        return Wall

    @classmethod
    def get_container_class(cls, base):
        class Container(cls._get_base_class(base)):
            def copy(self):
                clone = super().copy()
                for w in self.simple_text_set.all():
                    clone.simple_text_set.add(w.copy())

                for w in self.url_set.all():
                    clone.url_set.add(w.copy())

                for w in self.simple_list_set.all():
                    clone.simple_list_set.add(w.copy())

                for w in self.counter_set.all():
                    clone.counter_set.add(w.copy())

                for w in self.simple_switch_set.all():
                    clone.simple_switch_set.add(w.copy())

                for w in self.document_set.all():
                    clone.document_set.add(w.copy())
                clone.save()
                return clone

            class Meta:
                abstract = True

        return Container

    @classmethod
    def get_port_class(cls, base):
        return cls._get_base_class(base)

    @classmethod
    def get_source_class(cls, base):
        return cls._get_base_class(base)

    @classmethod
    def get_simple_text_class(cls, base):
        return cls._get_base_class(base)

    @classmethod
    def get_url_class(cls, base):
        return cls._get_base_class(base)

    @classmethod
    def get_simple_list_class(cls, base):
        return cls._get_base_class(base)

    @classmethod
    def get_counter_class(cls, base):
        return cls._get_base_class(base)

    @classmethod
    def get_simple_switch_class(cls, base):
        return cls._get_base_class(base)

    @classmethod
    def get_document_class(cls, base):
        return cls._get_base_class(base)
