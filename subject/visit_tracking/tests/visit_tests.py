from django.test import TestCase

from core.bhp_content_type_map.classes import ContentTypeMapHelper
from core.bhp_content_type_map.models import ContentTypeMap
from core.bhp_variables.tests.factories import StudySpecificFactory, StudySiteFactory
from subject.appointment.models import Appointment
from subject.consent.tests.factories import ConsentCatalogueFactory
from subject.lab_tracker.classes import site_lab_tracker
from subject.registration.models import RegisteredSubject
from testing.classes import TestVisitSchedule
from testing.tests.factories import TestConsentWithMixinFactory
from testing.models import TestOffStudy


class VisitTests(TestCase):

    app_label = 'testing'

    def setUp(self):
        site_lab_tracker.autodiscover()
        StudySpecificFactory()
        study_site = StudySiteFactory()
        content_type_map_helper = ContentTypeMapHelper()
        content_type_map_helper.populate()
        content_type_map_helper.sync()

        content_type_map = ContentTypeMap.objects.get(content_type__model='testconsentwithmixin')
        consent_catalogue = ConsentCatalogueFactory(name='v1', content_type_map=content_type_map)
        consent_catalogue.add_for_app = 'bhp_base_test'
        consent_catalogue.save()

        self.test_visit_schedule = TestVisitSchedule()
        self.test_visit_schedule.build()

    def test_off_study_reason(self):
        from testing.tests.factories import TestVisitFactory
        # add consent
        TestConsentWithMixinFactory(gender='M')
        registered_subject = RegisteredSubject.objects.all()[0]
        appointment = Appointment.objects.get(registered_subject=registered_subject)
        # add visit
        test_visit = TestVisitFactory(appointment=appointment)
        # assert no off study form
        self.assertEqual(TestOffStudy.objects.all().count(), 0)
        # add visit tracking
        test_visit.reason = 'off_study'
        test_visit.save()
        #assert off study form entry was created (additional)
        self.assertTrue(TestOffStudy.objects.all(), 1)
