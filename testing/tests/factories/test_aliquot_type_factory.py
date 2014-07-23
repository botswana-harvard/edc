import factory

from base.model.tests.factories import BaseUuidModelFactory

from ...models import TestAliquotType


class TestAliquotTypeFactory(BaseUuidModelFactory):
    FACTORY_FOR = TestAliquotType
