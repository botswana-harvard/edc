import factory
from edc_lab.lab_requisition.tests.factories import BaseRequisitionFactory
from ...models import TestRequisition
from .test_visit_factory import TestVisitFactory


class TestRequisitionFactory(BaseRequisitionFactory):
    FACTORY_FOR = TestRequisition

    test_visit = factory.SubFactory(TestVisitFactory)
