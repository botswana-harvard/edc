from edc.base.model.tests.factories import BaseUuidModelFactory
from ...models import TestScheduledModel


class TestScheduledModelFactory(BaseUuidModelFactory):
    FACTORY_FOR = TestScheduledModel
