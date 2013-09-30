import factory
from edc.core.bhp_base_model.tests.factories import BaseUuidModelFactory
from ...models import TestModel
from .test_foreign_key_factory import TestForeignKeyFactory


class TestModelFactory(BaseUuidModelFactory):
    FACTORY_FOR = TestModel

    name = factory.Sequence(lambda n: 'NAME{0}'.format(n))
    test_foreign_key = factory.SubFactory(TestForeignKeyFactory)
