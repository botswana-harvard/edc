from django.contrib import admin
from django.test import TestCase
from django.contrib.contenttypes.models import ContentType
from edc.core.bhp_content_type_map.classes import ContentTypeMapHelper
from edc.subject.entry.tests.factories import ScheduledEntryBucketFactory, EntryFactory
from edc.subject.registration.tests.factories import RegisteredSubjectFactory
from edc.subject.appointment.tests.factories import AppointmentFactory, ConfigurationFactory
from edc.core.bhp_base_test.tests.factories import TestVisitFactory, TestScheduledModelFactory
from edc.core.bhp_base_test.models import TestVisit, TestScheduledModel
from edc.subject.visit_schedule.tests.factories import VisitDefinitionFactory
from edc.core.bhp_content_type_map.models import ContentTypeMap
from edc.subject.entry.models import Entry
from ..classes import ScheduledEntryContext


class ScheduledEntryContextTests(TestCase):

    def test_p1(self):
        admin.autodiscover()
        content_type_map_helper = ContentTypeMapHelper()
        content_type_map_helper.populate()
        content_type_map_helper.sync()
        ConfigurationFactory()
        registered_subject = RegisteredSubjectFactory()
        content_type = ContentType.objects.get(app_label='bhp_base_test', model='testvisit')
        visit_tracking_content_type_map = ContentTypeMap.objects.get(content_type=content_type)
        visit_definition = VisitDefinitionFactory(visit_tracking_content_type_map=visit_tracking_content_type_map)
        appointment = AppointmentFactory(registered_subject=registered_subject, visit_definition=visit_definition)
        content_type = ContentType.objects.get(app_label='bhp_base_test', model='testscheduledmodel')
        content_type_map = ContentTypeMap.objects.get(content_type=content_type)
        entry = EntryFactory(visit_definition=visit_definition, content_type_map=content_type_map)
        scheduled_entry_bucket = ScheduledEntryBucketFactory(appointment=appointment, entry=entry)
        test_visit = TestVisitFactory(appointment=appointment)
        test_scheduled_model = TestScheduledModelFactory(test_visit=test_visit)
        inst = ScheduledEntryContext(scheduled_entry_bucket, appointment, TestVisit)

        self.assertEqual(inst.get_scheduled_entry(), scheduled_entry_bucket)
        print 'try to reverse scheduled_entry for pk={0}'.format(inst.get_scheduled_entry().pk)
        self.assertIsNotNone(inst.get_scheduled_entry().pk)
        self.assertIsNotNone(inst.get_scheduled_entry().pk)
        self.assertEqual(inst.get_visit_model(), TestVisit)
        self.assertEqual(inst.get_appointment(), appointment)

        self.assertEqual(inst.get_entry(), inst.get_scheduled_entry().entry)
        self.assertTrue(isinstance(inst.get_entry(), Entry))

        self.assertEqual(inst.get_app_label(), 'bhp_base_test')
        self.assertEqual(inst.get_model_name(), 'testscheduledmodel')
        self.assertEqual(inst.get_model_cls(), TestScheduledModel)
        self.assertIsNotNone(inst.get_model_pk())

        inst.get_context()
        #print inst.get_context()
        self.assertIsNotNone(inst.get_scheduled_entry_url())
