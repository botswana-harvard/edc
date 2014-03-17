import factory

from edc.base.model.tests.factories import BaseUuidModelFactory

from ...models import TestPanel

#from .test_aliquot_type_factory import TestAliquotTypeFactory


class TestPanelFactory(BaseUuidModelFactory):
    FACTORY_FOR = TestPanel

    name = factory.Sequence(lambda n: 'Panel {0}'.format(n))

    #aliquot_type = factory.SubFactory(TestAliquotTypeFactory)
