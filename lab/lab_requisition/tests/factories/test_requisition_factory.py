import factory
from testing.models import TestRequisition
from .base_clinic_requisition_factory import BaseClinicRequisitionFactory


class TestRequisitionFactory(BaseClinicRequisitionFactory):
    FACTORY_FOR = TestRequisition

    test_visit = None
