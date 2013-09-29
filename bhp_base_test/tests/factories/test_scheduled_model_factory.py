from edc_core.bhp_base_model.tests.factories import BaseUuidModelFactory
from ...models import TestScheduledModel


class TestScheduledModelFactory(BaseUuidModelFactory):
    FACTORY_FOR = TestScheduledModel
