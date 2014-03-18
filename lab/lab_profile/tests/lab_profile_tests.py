from datetime import datetime

from django.test import TestCase

from edc.entry_meta_data.models import RequisitionMetaData
from edc.lab.lab_clinic_api.models import Receive, Aliquot
from edc.lab.lab_profile.classes import site_lab_profiles
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.subject.appointment.models import Appointment
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.registration.models import RegisteredSubject
from edc.subject.visit_schedule.models import VisitDefinition
from edc.testing.classes import TestAppConfiguration
from edc.testing.classes import TestLabProfile
from edc.testing.classes import TestVisitSchedule
from edc.testing.tests.factories import TestConsentWithMixinFactory, TestRequisitionFactory
from edc.testing.models import TestPanel, TestAliquotType

from ..classes import LabProfile


class LabProfileTests(TestCase):

    def setUp(self):
        from edc.testing.tests.factories import TestVisitFactory
        self.test_visit_factory = TestVisitFactory
        site_lab_tracker.autodiscover()
        try:
            site_lab_profiles.register(TestLabProfile())
        except AlreadyRegisteredLabProfile:
            pass
        TestAppConfiguration()
        site_lab_tracker.autodiscover()
        TestVisitSchedule().build()
        self.visit_definition = VisitDefinition.objects.get(code='1000')
        self.test_consent = TestConsentWithMixinFactory(gender='M')
        self.registered_subject = RegisteredSubject.objects.get(subject_identifier=self.test_consent.subject_identifier)
        self.appointment = Appointment.objects.get(registered_subject=self.registered_subject)

    def test_receives1(self):
        """assert received if drawn."""
        self.test_visit = self.test_visit_factory(appointment=self.appointment)
        requisition_panel = RequisitionMetaData.objects.filter(registered_subject=self.registered_subject)[0].lab_entry.requisition_panel
        panel = TestPanel.objects.get(name=requisition_panel.name)
        aliquot_type = TestAliquotType.objects.get(alpha_code=requisition_panel.aliquot_type_alpha_code)
        obj = TestRequisitionFactory(test_visit=self.test_visit, panel=panel, aliquot_type=aliquot_type, is_drawn='Yes')
        lab_profile = LabProfile()
        self.assertTrue(lab_profile.receive(obj))
        self.assertEqual(Receive.objects.get(requisition_identifier=obj.requisition_identifier).requisition_identifier, obj.requisition_identifier)
        receive = Receive.objects.get(requisition_identifier=obj.requisition_identifier)
        self.assertEqual(Aliquot.objects.get(receive=receive).receive, receive)

    def test_receives2(self):
        self.test_visit = self.test_visit_factory(appointment=self.appointment)
        requisition_panel = RequisitionMetaData.objects.filter(registered_subject=self.registered_subject)[0].lab_entry.requisition_panel
        panel = TestPanel.objects.get(name=requisition_panel.name)
        aliquot_type = TestAliquotType.objects.get(alpha_code=requisition_panel.aliquot_type_alpha_code)
        obj = TestRequisitionFactory(test_visit=self.test_visit, panel=panel, aliquot_type=aliquot_type, is_drawn='No')
        lab_profile = LabProfile()
        self.assertFalse(lab_profile.receive(obj))

    def test_receives3(self):
        self.test_visit = self.test_visit_factory(appointment=self.appointment)
        requisition_panel = RequisitionMetaData.objects.filter(registered_subject=self.registered_subject)[0].lab_entry.requisition_panel
        panel = TestPanel.objects.get(name=requisition_panel.name)
        aliquot_type = TestAliquotType.objects.get(alpha_code=requisition_panel.aliquot_type_alpha_code)
        obj = TestRequisitionFactory(test_visit=self.test_visit, panel=panel, aliquot_type=aliquot_type, is_drawn='Yes')
        lab_profile = LabProfile()
        lab_profile.receive(obj)
        receive = Receive.objects.get(requisition_identifier=obj.requisition_identifier)
        print Aliquot.objects.get(receive=receive).__dict__
