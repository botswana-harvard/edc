import factory

from ...models import TestAliquotType


class TestAliquotTypeFactory(factory.DjangoModelFactory):
    class Meta:
        model = TestAliquotType
