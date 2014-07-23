from base.model.tests.factories import BaseUuidModelFactory
from subject.visit_tracking.tests.factories import BaseVisitTrackingFactory

from ...models import TestVisit


class TestVisitFactory(BaseVisitTrackingFactory):
    FACTORY_FOR = TestVisit


class TestSimpleVisitFactory(BaseUuidModelFactory):
    FACTORY_FOR = TestVisit
