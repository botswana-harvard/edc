from edc.core.bhp_base_model.tests.factories import BaseListModelFactory
from ...models import TestForeignKey


class TestForeignKeyFactory(BaseListModelFactory):
    FACTORY_FOR = TestForeignKey
