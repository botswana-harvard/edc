import factory
from edc.core.bhp_base_test.models import TestRequisition
from edc.core.bhp_base_test.tests.factories import TestVisitFactory
from .base_clinic_requisition_factory import BaseClinicRequisitionFactory


class TestRequisitionFactory(BaseClinicRequisitionFactory):
    FACTORY_FOR = TestRequisition

    test_visit = factory.SubFactory(TestVisitFactory)
