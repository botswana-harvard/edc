from datetime import datetime

from django.core.exceptions import ValidationError

from edc.core.bhp_content_type_map.classes import ContentTypeMapHelper
from edc.core.bhp_content_type_map.models import ContentTypeMap
from edc.core.bhp_variables.tests.factories import StudySpecificFactory, StudySiteFactory
from edc.entry_meta_data.models import ScheduledEntryMetaData
from edc.subject.consent.tests.factories import ConsentCatalogueFactory
from edc.subject.entry.tests.factories import EntryFactory
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.registration.models import RegisteredSubject
from edc.subject.visit_schedule.models import VisitDefinition
from edc.subject.visit_schedule.tests.factories import MembershipFormFactory, ScheduleGroupFactory, VisitDefinitionFactory
from edc.testing.models import TestConsent, TestScheduledModel

from ..choices import APPT_STATUS
from ..models import Appointment

from .base_appointment_tests import BaseAppointmentTests


class TestQualityInspection(BaseAppointmentTests):

    def test_close_off_appointment(self):
        from edc.testing.tests.factories import TestRegistrationFactory, TestVisitFactory, TestConsentFactory, TestScheduledModelFactory
        app_label = 'bhp_base_test'
        site_lab_tracker.autodiscover()
        StudySpecificFactory()
        StudySiteFactory()
        content_type_map_helper = ContentTypeMapHelper()
        content_type_map_helper.populate()
        content_type_map_helper.sync()
        print 'setup the consent catalogue for app {0}'.format(app_label)
        content_type_map = ContentTypeMap.objects.get(content_type__model=TestConsent._meta.object_name.lower())
        consent_catalogue = ConsentCatalogueFactory(name='c1', content_type_map=content_type_map)
        consent_catalogue.add_for_app = 'bhp_base_test'
        consent_catalogue.save()

        print 'setup visit T0.0'
        content_type_map = ContentTypeMap.objects.get(content_type__model='testregistration')
        visit_tracking_content_type_map = ContentTypeMap.objects.get(content_type__model='testvisit')
        membership_form = MembershipFormFactory(content_type_map=content_type_map)
        schedule_group = ScheduleGroupFactory(membership_form=membership_form, group_name='Test Reg', grouping_key='REGISTRATION')
        visit_definition = VisitDefinitionFactory(code='T0', title='Baseline', grouping='test_subject',
                                                  time_point=0,
                                                  base_interval=0,
                                                  base_interval_unit='D',
                                                  visit_tracking_content_type_map=visit_tracking_content_type_map)
        visit_definition.schedule_group.add(schedule_group)
        # adding a consent
        test_consent = TestConsentFactory()
        # add registration
        registered_subject = RegisteredSubject.objects.get(subject_identifier=test_consent.subject_identifier)
        self.assertEquals(Appointment.objects.all().count(), 0)

        print 'Registering Subject'
        test_registration = TestRegistrationFactory(registered_subject=registered_subject)

        print 'assert a T0.0 appointment has been created'
        self.assertEquals(Appointment.objects.all().count(), 1)

        print 'assert appointment is new'
        for appointment in Appointment.objects.all():
            self.assertEqual(appointment.appt_status, 'new')

        print 'get appointment T0'
        appointment = Appointment.objects.get(registered_subject=registered_subject, visit_definition__code='T0')

        print 'make appointment visit reason to be scheduled'
        test_visit = TestVisitFactory(appointment=appointment, reason='scheduled')

        print 'check that the appointment is now in_progress'
        self.assertEquals(appointment.appt_status, 'in_progress')

        for appt_status in APPT_STATUS:
            print 'getting appointment T0 with visit instance set to zero'
            appointment = Appointment.objects.get(registered_subject=registered_subject, visit_definition__code='T0', visit_instance='0')
            print 'The T0.0 appointment status is {0}'.format(appointment.appt_status)
        if appt_status[0] == 'done':
                appointment.save()
                print 'assert appointment status changed to done'
                self.assertEquals(appointment.appt_status, 'done')
        if appointment.appt_status == 'done':
            print 'confirm entry into Quality Inspection form'
            from edc.core.bhp_data_manager.tests.factories import QualityInspectionFactory
            from edc.core.bhp_data_manager.models import QualityInspection
            quality = QualityInspectionFactory(registered_subject=registered_subject, the_visit_code=visit_definition.code)
            self.asserEqual(QualityInspection.objects.all().count(), 1)
            print quality
