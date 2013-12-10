from django.test import TestCase

from edc.core.bhp_content_type_map.classes import ContentTypeMapHelper
from edc.testing.classes import TestVisitSchedule
from edc.subject.entry.models import Entry, LabEntry
from edc.subject.appointment_helper.models import BaseAppointmentMixin
from edc.testing.tests.factories import TestConsentWithMixinFactory
from edc.subject.appointment.tests.factories import ConfigurationFactory

from ..models import MembershipForm, ScheduleGroup, VisitDefinition

from ..classes import MembershipFormTuple, ScheduleGroupTuple


class VisitScheduleTests(TestCase):

    def setUp(self):
        ConfigurationFactory()
        content_type_map_helper = ContentTypeMapHelper()
        content_type_map_helper.populate()
        content_type_map_helper.sync()

        self.test_visit_schedule = TestVisitSchedule()
        self.test_visit_schedule.build()

    def test_build_membership_form(self):
        """Creates as many instances of membership_form as in the config."""
        self.assertEqual(MembershipForm.objects.count(), len(self.test_visit_schedule.membership_forms.values()))

    def test_build_schedule_group(self):
        """Creates as many instances of schedule_group as in the config."""
        self.assertEqual(ScheduleGroup.objects.count(), len(self.test_visit_schedule.schedule_groups.values()))

    def test_build_visit_definition(self):
        """Creates as many instances of visit_definition as in the config."""
        self.assertEqual(VisitDefinition.objects.count(), len(self.test_visit_schedule.visit_definitions.values()))

    def test_build_entry(self):
        """Creates as many instances of entry as in the config."""
        for visit_definition_name in self.test_visit_schedule.visit_definitions:
            self.assertEqual(Entry.objects.count(), len(self.test_visit_schedule.visit_definitions[visit_definition_name].get('entries')))
        self.assertGreater(Entry.objects.count(), 0)

    def test_build_lab_entry(self):
        """Creates as many instances of lab_entry as in the config."""
        for visit_definition_name in self.test_visit_schedule.visit_definitions:
            self.assertEqual(LabEntry.objects.count(), len(self.test_visit_schedule.visit_definitions[visit_definition_name].get('requisitions')))
        self.assertGreater(LabEntry.objects.count(), 0)

    def test_visit_definition_knows_membership_form(self):
        """Visit definition knows the MembershipForm and the model is a subclass of BaseAppointmentMixin"""
        for visit_definition_name in self.test_visit_schedule.visit_definitions:
            schedule_group_name = self.test_visit_schedule.visit_definitions.get(visit_definition_name).get('schedule_group')
            schedule_group = self.test_visit_schedule.schedule_groups.get(schedule_group_name)
            # the membership_form named tuple in dictionary test_visit_schedule.membership_forms.
            self.assertTrue(issubclass(self.test_visit_schedule.membership_forms.get(schedule_group.membership_form_name).__class__, MembershipFormTuple))
            # the model in the membership_form named tuple.
            self.assertTrue(issubclass(self.test_visit_schedule.membership_forms.get(schedule_group.membership_form_name).model, BaseAppointmentMixin))

    def test_visit_definition_knows_schedule_group(self):
        """Visit definition knows ScheduleGroup and it is a subclass of the named tuple."""
        for visit_definition_name in self.test_visit_schedule.visit_definitions:
            schedule_group_name = self.test_visit_schedule.visit_definitions.get(visit_definition_name).get('schedule_group')
            self.assertTrue(issubclass(self.test_visit_schedule.schedule_groups.get(schedule_group_name).__class__, ScheduleGroupTuple))

    def test_can_create_membership_form_model_instance(self):
        """Can create and instance of the membership form model."""
        for visit_definition_name in self.test_visit_schedule.visit_definitions:
            schedule_group_name = self.test_visit_schedule.visit_definitions[visit_definition_name].get('schedule_group')
            schedule_group = self.test_visit_schedule.schedule_groups.get(schedule_group_name)
            membership_form_model = self.test_visit_schedule.membership_forms[schedule_group.membership_form_name].model
            # i know this is a consent model in the test case
            self.assertEqual(membership_form_model, TestConsentWithMixinFactory.FACTORY_FOR)
            self.assertIsNotNone(TestConsentWithMixinFactory(gender='M'))