import factory

from edc.lab.lab_requisition.tests.factories import BaseRequisitionFactory

from ...models import TestRequisition

from edc_visit_tracking.tests.factories import TestVisitFactory


class TestRequisitionFactory(BaseRequisitionFactory):
    class Meta:
        model = TestRequisition

    test_visit = factory.SubFactory(TestVisitFactory)
