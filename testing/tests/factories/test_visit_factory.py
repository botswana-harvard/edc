
from edc.base.model.tests.factories import BaseUuidModelFactory
from edc.subject.visit_tracking.tests.factories import BaseVisitTrackingFactory
from ...models import TestVisit


class TestVisitFactory(BaseVisitTrackingFactory):
    FACTORY_FOR = TestVisit


class TestSimpleVisitFactory(BaseUuidModelFactory):
    FACTORY_FOR = TestVisit
