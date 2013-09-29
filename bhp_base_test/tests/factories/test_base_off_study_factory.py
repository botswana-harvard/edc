from edc_core.bhp_off_study.tests.factories import BaseOffStudyFactory
from ...models import TestBaseOffStudy


class TestBaseOffStudyFactory(BaseOffStudyFactory):
    FACTORY_FOR = TestBaseOffStudy
