from edc.subject.off_study.tests.factories import BaseOffStudyFactory
from ...models import TestBaseOffStudy


class TestBaseOffStudyFactory(BaseOffStudyFactory):
    FACTORY_FOR = TestBaseOffStudy
