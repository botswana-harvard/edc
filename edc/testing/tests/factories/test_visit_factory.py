from edc.base.model.tests.factories import BaseUuidModelFactory
from edc.subject.visit_tracking.tests.factories import BaseVisitTrackingFactory

from ...models import TestVisit


class TestVisitFactory(BaseVisitTrackingFactory):
    class Meta:
        model = TestVisit


class TestSimpleVisitFactory(BaseUuidModelFactory):
    class Meta:
        model = TestVisit
