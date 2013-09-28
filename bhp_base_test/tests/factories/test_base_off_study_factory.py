import factory
from edc_lib.bhp_off_study.tests.factories import BaseOffStudyFactory
from edc_lib.bhp_base_test.models import TestBaseOffStudy


class TestBaseOffStudyFactory(BaseOffStudyFactory):
    FACTORY_FOR = TestBaseOffStudy
