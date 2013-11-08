from django.test import TestCase

from edc.core.bhp_content_type_map.classes import ContentTypeMapHelper
from edc.core.bhp_content_type_map.models import ContentTypeMap
from edc.core.bhp_variables.tests.factories import StudySpecificFactory, StudySiteFactory
from edc.subject.appointment.models import Appointment
from edc.subject.appointment.tests.factories import ConfigurationFactory
from edc.subject.consent.tests.factories import ConsentCatalogueFactory
from edc.subject.entry.tests.factories import EntryFactory
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.registration.models import RegisteredSubject
from edc.subject.visit_schedule.tests.factories import MembershipFormFactory, ScheduleGroupFactory, VisitDefinitionFactory


class VisitTests(TestCase):

    def test_p1(self):
        from edc.testing.tests.factories import TestRegistrationFactory, TestVisitFactory, TestConsentFactory
        site_lab_tracker.autodiscover()
        StudySpecificFactory()
        study_site = StudySiteFactory()
        ConfigurationFactory()
        app_label = 'testing'

        content_type_map_helper = ContentTypeMapHelper()
        content_type_map_helper.populate()
        content_type_map_helper.sync()

        print 'setup the consent catalogue for app {0}'.format(app_label)
        content_type_map = ContentTypeMap.objects.get(content_type__model='testconsent')
        consent_catalogue = ConsentCatalogueFactory(name='v1', content_type_map=content_type_map)
        consent_catalogue.add_for_app = 'bhp_base_test'
        consent_catalogue.save()

        print 'setup bhp_visit (1000, 1010, 1020, 1030)'
        content_type_map = ContentTypeMap.objects.get(content_type__model='testregistration')
        visit_tracking_content_type_map = ContentTypeMap.objects.get(content_type__model='testvisit')
        membership_form = MembershipFormFactory(content_type_map=content_type_map)
        schedule_group = ScheduleGroupFactory(membership_form=membership_form, group_name='Test Reg', grouping_key='REGISTRATION')
        visit_definition = VisitDefinitionFactory(code='1000', title='Test Registration 00', grouping='test_subject', 
                                                  time_point=0,
                                                  base_interval=0,
                                                  base_interval_unit='D',
                                                  visit_tracking_content_type_map=visit_tracking_content_type_map)
        visit_definition.schedule_group.add(schedule_group)
        visit_definition = VisitDefinitionFactory(code='1010', title='Test Registration 10', grouping='test_subject',
                                                  time_point=10,
                                                  base_interval=1,
                                                  base_interval_unit='M',
                                                  visit_tracking_content_type_map=visit_tracking_content_type_map)
        visit_definition.schedule_group.add(schedule_group)
        content_type_map = ContentTypeMap.objects.get(content_type__model='testscheduledmodel')
        EntryFactory(visit_definition=visit_definition, content_type_map=content_type_map)

        visit_definition = VisitDefinitionFactory(code='1020', title='Test Registration 20', grouping='test_subject',
                                                  time_point=20,
                                                  base_interval=2,
                                                  base_interval_unit='M',
                                                  visit_tracking_content_type_map=visit_tracking_content_type_map)
        visit_definition.schedule_group.add(schedule_group)
        visit_definition = VisitDefinitionFactory(code='1030', title='Test Registration 30', grouping='test_subject',
                                                  time_point=30,
                                                  base_interval=3,
                                                  base_interval_unit='M',
                                                  visit_tracking_content_type_map=visit_tracking_content_type_map)
        visit_definition.schedule_group.add(schedule_group)
        # add consent
        test_consent = TestConsentFactory()
        # add registration
        registered_subject = RegisteredSubject.objects.get(subject_identifier=test_consent.subject_identifier)
        self.assertEquals(Appointment.objects.all().count(), 0)
        print 'complete a registration form'
        test_registration = TestRegistrationFactory(registered_subject=registered_subject)
        print 'assert 4 appointments created'
        self.assertEquals(Appointment.objects.all().count(), 4)

        print 'add visit tracking for 1000'
        appointment = Appointment.objects.get(visit_definition__code='1000')
        TestVisitFactory(appointment=appointment)
        print 'assert no off study form'
        print 'add visit tracking for 1010 reason off study'
        appointment = Appointment.objects.get(visit_definition__code='1010')
        TestVisitFactory(appointment=appointment, reason='off_study')
        print 'assert off study form entry was created (additional)'
