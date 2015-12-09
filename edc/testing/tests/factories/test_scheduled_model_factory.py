from edc.base.model.tests.factories import BaseUuidModelFactory

from ...models import TestScheduledModel, TestScheduledModel1, TestScheduledModel2, TestScheduledModel3


class TestScheduledModelFactory(BaseUuidModelFactory):
    class Meta:
        model = TestScheduledModel


class TestScheduledModel1Factory(BaseUuidModelFactory):
    class Meta:
        model = TestScheduledModel1


class TestScheduledModel2Factory(BaseUuidModelFactory):
    class Meta:
        model = TestScheduledModel2


class TestScheduledModel3Factory(BaseUuidModelFactory):
    class Meta:
        model = TestScheduledModel3
