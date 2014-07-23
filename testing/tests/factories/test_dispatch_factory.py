import factory
from base.model.tests.factories import BaseUuidModelFactory
from ...models import TestDspContainer, TestDspItemBypass, TestDspItem


class TestDspContainerFactory(BaseUuidModelFactory):
    FACTORY_FOR = TestDspContainer

    test_container_identifier = factory.Sequence(lambda n: 'CONTAINER_ID{0}'.format(n))
    comment = 'test_container'


class TestDspItemBypassFactory(BaseUuidModelFactory):
    FACTORY_FOR = TestDspItemBypass

    test_item_identifier = factory.Sequence(lambda n: 'ITEM_BYPASS_ID{0}'.format(n))
    test_container = factory.SubFactory(TestDspContainerFactory)
    f1 = factory.Sequence(lambda n: 'F1_{0}'.format(n))
    f2 = factory.Sequence(lambda n: 'F2_{0}'.format(n))
    f3 = factory.Sequence(lambda n: 'F3_{0}'.format(n))
    f4 = factory.Sequence(lambda n: 'F4_{0}'.format(n))


class TestDspItemFactory(BaseUuidModelFactory):
    FACTORY_FOR = TestDspItem

    test_item_identifier = factory.Sequence(lambda n: 'ITEM_ID{0}'.format(n))
    test_container = factory.SubFactory(TestDspContainerFactory)
