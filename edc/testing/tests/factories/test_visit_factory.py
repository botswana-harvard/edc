from edc_visit_tracking.tests.factories import BaseVisitTrackingFactory

from ...models import TestVisit


class TestVisitFactory(BaseVisitTrackingFactory):
    class Meta:
        model = TestVisit

