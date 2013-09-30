import factory
from edc.lab.lab_base_model.tests.factories import BaseLabModelFactory
from ...models import PanelGroup


class PanelGroupFactory(BaseLabModelFactory):
    FACTORY_FOR = PanelGroup

    name = factory.Sequence(lambda n: 'panelgroup{0}'.format(n))
