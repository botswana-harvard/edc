import factory

from ...models import TestScheduledModel, TestScheduledModel1, TestScheduledModel2, TestScheduledModel3


class TestScheduledModelFactory(factory.DjangoModelFactory):
    class Meta:
        model = TestScheduledModel


class TestScheduledModel1Factory(factory.DjangoModelFactory):
    class Meta:
        model = TestScheduledModel1


class TestScheduledModel2Factory(factory.DjangoModelFactory):
    class Meta:
        model = TestScheduledModel2


class TestScheduledModel3Factory(factory.DjangoModelFactory):
    class Meta:
        model = TestScheduledModel3
