import factory
from edc.core.bhp_base_model.tests.factories import BaseUuidModelFactory
from ...models import TestDispatchContainer, TestDispatchItemBypassForEdit, TestDispatchItem


class TestDispatchContainerFactory(BaseUuidModelFactory):
    FACTORY_FOR = TestDispatchContainer

    test_container_identifier = factory.Sequence(lambda n: 'CONTAINER_ID{0}'.format(n))
    comment = 'test_container'


class TestDispatchItemBypassForEditFactory(BaseUuidModelFactory):
    FACTORY_FOR = TestDispatchItemBypassForEdit

    test_item_identifier = factory.Sequence(lambda n: 'ITEM_BYPASS_ID{0}'.format(n))
    test_container = factory.SubFactory(TestDispatchContainerFactory)
    f1 = factory.Sequence(lambda n: 'F1_{0}'.format(n))
    f2 = factory.Sequence(lambda n: 'F2_{0}'.format(n))
    f3 = factory.Sequence(lambda n: 'F3_{0}'.format(n))
    f4 = factory.Sequence(lambda n: 'F4_{0}'.format(n))


class TestDispatchItemFactory(BaseUuidModelFactory):
    FACTORY_FOR = TestDispatchItem

    test_item_identifier = factory.Sequence(lambda n: 'ITEM_ID{0}'.format(n))
    test_container = factory.SubFactory(TestDispatchContainerFactory)
