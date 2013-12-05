from edc.base.model.tests.factories import BaseUuidModelFactory
from ...models import TestScheduledModel, TestScheduledModel1, TestScheduledModel2, TestScheduledModel3


class TestScheduledModelFactory(BaseUuidModelFactory):
    FACTORY_FOR = TestScheduledModel


class TestScheduledModel1Factory(BaseUuidModelFactory):
    FACTORY_FOR = TestScheduledModel1


class TestScheduledModel2Factory(BaseUuidModelFactory):
    FACTORY_FOR = TestScheduledModel2


class TestScheduledModel3Factory(BaseUuidModelFactory):
    FACTORY_FOR = TestScheduledModel3
