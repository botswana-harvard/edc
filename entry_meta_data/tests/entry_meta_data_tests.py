from datetime import datetime

from django.test import TestCase

from edc.core.bhp_content_type_map.classes import ContentTypeMapHelper
from edc.core.bhp_content_type_map.models import ContentTypeMap
from edc.core.bhp_variables.tests.factories import StudySpecificFactory, StudySiteFactory
from edc.entry_meta_data.models import ScheduledEntryMetaData, RequisitionMetaData
from edc.subject.appointment.models import Appointment
from edc.subject.appointment.tests.factories import ConfigurationFactory
from edc.subject.consent.tests.factories import ConsentCatalogueFactory
from edc.subject.entry.exceptions import EntryManagerError
from edc.subject.entry.models import Entry, LabEntry
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.registration.models import RegisteredSubject
from edc.subject.visit_schedule.models import VisitDefinition
from edc.subject.visit_schedule.tests.factories import MembershipFormFactory, ScheduleGroupFactory, VisitDefinitionFactory
from edc.testing.classes import TestVisitSchedule
from edc.testing.tests.factories import TestConsentWithMixinFactory, TestScheduledModel1Factory, TestRequisitionFactory


class EntryMetaDataTests(TestCase):

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
        #self.test_visit = self.test_visit_factory(appointment=self.appointment)

#     def model_for_entry_requires_manager(self):
#         content_type_map = ContentTypeMap.objects.get(app_label='testing', model='testscheduledmodel')
#         self.assertRaises(EntryManagerError, EntryFactory, content_type_map=content_type_map, visit_definition=self.visit_definition, entry_order=10, entry_category='clinic')

    def test_creates_meta_data1(self):
        """No meta data if visit tracking form is not entered."""
        self.assertEqual(ScheduledEntryMetaData.objects.filter(registered_subject=self.registered_subject).count(), 0)

    def test_creates_requisition_meta_data(self):
        """Meta data is created when visit tracking form is added, each instance set to NEW."""
        self.assertTrue(LabEntry.objects.all().count() > 0)
        self.test_visit = self.test_visit_factory(appointment=self.appointment)
        self.assertEqual(RequisitionMetaData.objects.filter(registered_subject=self.registered_subject).count(), 3)
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status='NEW', registered_subject=self.registered_subject).count(), 3)

    def test_creates_requisition_meta_data2(self):
        """Meta data is unchanged if you re-save visit."""
        self.assertTrue(LabEntry.objects.all().count() > 0)
        self.test_visit = self.test_visit_factory(appointment=self.appointment)
        self.test_visit.save()
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status='NEW', registered_subject=self.registered_subject).count(), 3)

    def test_updates_requisition_meta_data(self):
        self.test_visit = self.test_visit_factory(appointment=self.appointment)
        panel = RequisitionMetaData.objects.filter(registered_subject=self.registered_subject)[0].lab_entry.panel
        obj = TestRequisitionFactory(test_visit=self.test_visit, panel=panel)
        obj.save()
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status='KEYED',
                                                               registered_subject=self.registered_subject,
                                                               lab_entry__app_label='testing',
                                                               lab_entry__model_name='testrequisition',
                                                               lab_entry__panel=obj.panel).count(), 1)

    def test_updates_requisition_meta_data2(self):
        """Meta data is set to KEYED and is unchanged if you re-save requisition or re-save visit."""
        self.test_visit = self.test_visit_factory(appointment=self.appointment)
        panel = RequisitionMetaData.objects.filter(registered_subject=self.registered_subject)[0].lab_entry.panel
        obj = TestRequisitionFactory(test_visit=self.test_visit, panel=panel)
        obj.save()
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status='KEYED',
                                                               registered_subject=self.registered_subject,
                                                               lab_entry__app_label='testing',
                                                               lab_entry__model_name='testrequisition',
                                                               lab_entry__panel=obj.panel).count(), 1)
        self.test_visit.save()
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status='KEYED',
                                                               registered_subject=self.registered_subject,
                                                               lab_entry__app_label='testing',
                                                               lab_entry__model_name='testrequisition',
                                                               lab_entry__panel=obj.panel).count(), 1)
        obj.save()
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status='KEYED',
                                                               registered_subject=self.registered_subject,
                                                               lab_entry__app_label='testing',
                                                               lab_entry__model_name='testrequisition',
                                                               lab_entry__panel=obj.panel).count(), 1)

    def test_updates_requisition_meta_data_on_delete(self):
        """Meta data is set to KEYED and is unchanged if you re-save requisition or re-save visit."""
        self.test_visit = self.test_visit_factory(appointment=self.appointment)
        panel = RequisitionMetaData.objects.filter(registered_subject=self.registered_subject)[0].lab_entry.panel
        obj = TestRequisitionFactory(test_visit=self.test_visit, panel=panel)
        obj.save()
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status='KEYED',
                                                               registered_subject=self.registered_subject,
                                                               lab_entry__app_label='testing',
                                                               lab_entry__model_name='testrequisition',
                                                               lab_entry__panel=panel).count(), 1)
        obj.delete()
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status='NEW',
                                                               registered_subject=self.registered_subject,
                                                               lab_entry__app_label='testing',
                                                               lab_entry__model_name='testrequisition',
                                                               lab_entry__panel=panel).count(), 1)

    def test_creates_meta_data2(self):
        """Meta data is created when visit tracking form is added, each instance set to NEW."""
        self.test_visit = self.test_visit_factory(appointment=self.appointment)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='NEW', registered_subject=self.registered_subject).count(), 3)

    def test_creates_meta_data3(self):
        """Meta data is not re-created when visit tracking form is updated."""
        self.test_visit = self.test_visit_factory(appointment=self.appointment)
        TestScheduledModel1Factory(test_visit=self.test_visit)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='NEW', registered_subject=self.registered_subject).count(), 2)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='KEYED', registered_subject=self.registered_subject).count(), 1)

    def test_creates_meta_data4(self):
        """Meta data is deleted when visit tracking form is deleted."""
        self.test_visit = self.test_visit_factory(appointment=self.appointment)
        self.assertEqual(RequisitionMetaData.objects.filter(registered_subject=self.registered_subject).count(), 3)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(registered_subject=self.registered_subject).count(), 3)
        self.test_visit.delete()
        self.assertEqual(ScheduledEntryMetaData.objects.filter(registered_subject=self.registered_subject).count(), 0)
        self.assertEqual(RequisitionMetaData.objects.filter(registered_subject=self.registered_subject).count(), 0)

    def test_creates_meta_data5(self):
        """Meta data is not created if visit reason is missed. See 'skip_create_visit_reasons class' attribute"""
        self.test_visit = self.test_visit_factory(appointment=self.appointment, reason='missed')
        self.assertEqual(ScheduledEntryMetaData.objects.filter(registered_subject=self.registered_subject).count(), 0)

    def test_updates_meta_data4(self):
        """Meta data instance linked to the model is updated if model is entered."""
        self.test_visit = self.test_visit_factory(appointment=self.appointment)
        TestScheduledModel1Factory(test_visit=self.test_visit)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='KEYED', registered_subject=self.registered_subject, entry__content_type_map__model='testscheduledmodel1').count(), 1)

    def test_updates_meta_data5(self):
        """Meta data instance linked to the model is updated if model is entered and then updated."""
        self.test_visit = self.test_visit_factory(appointment=self.appointment)
        obj = TestScheduledModel1Factory(test_visit=self.test_visit)
        obj.save()
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='KEYED',
                                                               registered_subject=self.registered_subject,
                                                               entry__app_label='testing',
                                                               entry__model_name='testscheduledmodel1').count(), 1)

    def test_updates_meta_data6(self):
        """Meta data instance linked to the model is updated if model is deleted."""
        self.test_visit = self.test_visit_factory(appointment=self.appointment)
        obj = TestScheduledModel1Factory(test_visit=self.test_visit)
        obj.delete()
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='NEW', registered_subject=self.registered_subject, entry__content_type_map__model='testscheduledmodel1').count(), 1)

    def test_updates_meta_data7(self):
        """Meta data instance linked to the model is created if missing, knows model is KEYED."""
        self.test_visit = self.test_visit_factory(appointment=self.appointment)
        ScheduledEntryMetaData.objects.filter(entry_status='NEW', registered_subject=self.registered_subject, entry__model_name='testscheduledmodel1').delete()
        TestScheduledModel1Factory(test_visit=self.test_visit)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='KEYED', registered_subject=self.registered_subject, entry__model_name='testscheduledmodel1').count(), 1)