from ....bhp_visit_tracking.tests.factories import BaseVisitTrackingFactory
from ...models import TestVisit


class TestVisitFactory(BaseVisitTrackingFactory):
    FACTORY_FOR = TestVisit
