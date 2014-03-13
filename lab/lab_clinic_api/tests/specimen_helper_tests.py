from datetime import datetime

from django.test import TestCase

from edc.core.bhp_content_type_map.classes import ContentTypeMapHelper
from edc.core.bhp_content_type_map.models import ContentTypeMap
from edc.core.bhp_variables.tests.factories import StudySpecificFactory, StudySiteFactory
from edc.entry_meta_data.models import RequisitionMetaData
from edc.lab.lab_clinic_api.models import Receive, Aliquot
from edc.subject.appointment.models import Appointment
from edc.subject.appointment.tests.factories import ConfigurationFactory
from edc.subject.consent.tests.factories import ConsentCatalogueFactory
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.registration.models import RegisteredSubject
from edc.subject.visit_schedule.models import VisitDefinition
from edc.testing.classes import TestVisitSchedule
from edc.testing.tests.factories import TestConsentWithMixinFactory, TestRequisitionFactory

from ..classes import SpecimenHelper


class SpecimenHelperTests(TestCase):

    app_label = 'testing'
    consent_catalogue_name = 'v1'

    def setUp(self):
        from edc.testing.tests.factories import TestVisitFactory
        self.test_visit_factory = TestVisitFactory
        site_lab_tracker.autodiscover()
        study_specific = StudySpecificFactory()
        StudySiteFactory()
        ConfigurationFactory()
        content_type_map_helper = ContentTypeMapHelper()
        content_type_map_helper.populate()
        content_type_map_helper.sync()
        content_type_map = ContentTypeMap.objects.get(content_type__model='TestConsentWithMixin'.lower())
        ConsentCatalogueFactory(
            name=self.app_label,
            consent_type='study',
            content_type_map=content_type_map,
            version=1,
            start_datetime=study_specific.study_start_datetime,
            end_datetime=datetime(datetime.today().year + 5, 1, 1),
            add_for_app=self.app_label)

        test_visit_schedule = TestVisitSchedule()
        test_visit_schedule.rebuild()

        self.visit_definition = VisitDefinition.objects.get(code='1000')

        self.test_consent = TestConsentWithMixinFactory(gender='M')

        self.registered_subject = RegisteredSubject.objects.get(subject_identifier=self.test_consent.subject_identifier)
        self.appointment = Appointment.objects.get(registered_subject=self.registered_subject)

    def test_receives1(self):
        """assert received if drawn."""
        self.test_visit = self.test_visit_factory(appointment=self.appointment)
        panel = RequisitionMetaData.objects.filter(registered_subject=self.registered_subject)[0].lab_entry.panel
        obj = TestRequisitionFactory(test_visit=self.test_visit, panel=panel, is_drawn='Yes')
        specimen_helper = SpecimenHelper()
        self.assertTrue(specimen_helper.receive(obj))
        self.assertEqual(Receive.objects.get(requisition_identifier=obj.requisition_identifier).requisition_identifier, obj.requisition_identifier)
        receive = Receive.objects.get(requisition_identifier=obj.requisition_identifier)
        self.assertEqual(Aliquot.objects.get(receive=receive).receive, receive)

    def test_receives2(self):
        self.test_visit = self.test_visit_factory(appointment=self.appointment)
        panel = RequisitionMetaData.objects.filter(registered_subject=self.registered_subject)[0].lab_entry.panel
        obj = TestRequisitionFactory(test_visit=self.test_visit, panel=panel, is_drawn='No')
        specimen_helper = SpecimenHelper()
        self.assertFalse(specimen_helper.receive(obj))

    def test_receives3(self):
        self.test_visit = self.test_visit_factory(appointment=self.appointment)
        panel = RequisitionMetaData.objects.filter(registered_subject=self.registered_subject)[0].lab_entry.panel
        obj = TestRequisitionFactory(test_visit=self.test_visit, panel=panel, is_drawn='Yes')
        specimen_helper = SpecimenHelper()
        specimen_helper.receive(obj)
        receive = Receive.objects.get(requisition_identifier=obj.requisition_identifier)
        print Aliquot.objects.get(receive=receive).__dict__
