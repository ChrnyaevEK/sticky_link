from application.models.concrete import access_manager
from application.models.concrete import copy_manager
from application.models.concrete import general_declaration
from application.models.concrete import representation_manager
from application.models.concrete import routine_manager
from application.models.concrete import synchronization_manager
from application.models.concrete import type_declaration

from application.models import abstract

factory_list = [
    access_manager.ConcreteFactory,
    copy_manager.ConcreteFactory,
    general_declaration.ConcreteFactory,
    representation_manager.ConcreteFactory,
    routine_manager.ConcreteFactory,
    synchronization_manager.ConcreteFactory,
    type_declaration.ConcreteFactory
]


def get(base):
    # Iterate over managers and merge them into one big ancestor
    for factory in factory_list:
        base = factory.get(base)
    return base


class Wall(get(abstract.Wall)):
    pass


class Container(get(abstract.Container)):
    pass


class Port(get(abstract.Port)):
    pass


class Source(get(abstract.Source)):
    pass


class SimpleText(get(abstract.SimpleText)):
    pass


class URL(get(abstract.URL)):
    pass


class SimpleList(get(abstract.SimpleList)):
    pass


class Counter(get(abstract.Counter)):
    pass


class SimpleSwitch(get(abstract.SimpleSwitch)):
    pass


class Document(get(abstract.Document)):
    pass
