from edc.base.model.tests.factories import BaseListModelFactory
from ...models import TestManyToMany


class TestManyToManyFactory(BaseListModelFactory):
    FACTORY_FOR = TestManyToMany
