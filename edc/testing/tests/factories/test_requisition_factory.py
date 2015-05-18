import factory

from edc.lab.lab_requisition.tests.factories import BaseRequisitionFactory

from ...models import TestRequisition

from .test_visit_factory import TestVisitFactory


class TestRequisitionFactory(BaseRequisitionFactory):
    class Meta:
        model = TestRequisition

    test_visit = factory.SubFactory(TestVisitFactory)
