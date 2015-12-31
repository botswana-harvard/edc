import factory

from ...models import TestM2m


class TestM2mFactory(factory.DjangoModelFactory):
    class Meta:
        model = TestM2m
