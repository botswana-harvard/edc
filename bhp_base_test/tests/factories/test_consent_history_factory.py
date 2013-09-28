import factory
from edc_lib.bhp_base_model.tests.factories import BaseUuidModelFactory
from edc_lib.bhp_base_test.models import TestConsentHistory


class TestConsentHistoryFactory(BaseUuidModelFactory):
    FACTORY_FOR = TestConsentHistory
