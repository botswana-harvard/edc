from .base_test import BaseTest
from edc.testing.models import TestVisit
from edc_constants.constants import SCHEDULED
from django.utils import timezone
from edc.subject.appointment.models.appointment import Appointment
from edc.subject.visit_schedule.models.visit_definition import VisitDefinition
from edc.subject.visit_tracking.models.previous_visit_mixin import PreviousVisitError


class TestPreviousVisitMixin(BaseTest):

    def test_previous_visit_definition(self):
        TestVisit.REQUIRES_PREVIOUS_VISIT = False
        self.visit_definition = VisitDefinition.objects.get(code='2000')
        next_appointment = Appointment.objects.create(
            registered_subject=self.registered_subject,
            appt_datetime=timezone.now(),
            visit_definition=self.visit_definition)
        TestVisit.REQUIRES_PREVIOUS_VISIT = False
        test_visit = TestVisit.objects.create(
            appointment=next_appointment,
            report_datetime=timezone.now(),
            reason=SCHEDULED)
        self.assertEqual(test_visit.previous_visit_definition('2000').code, '1000')

    def test_previous_visit_doesnotexist(self):
        TestVisit.REQUIRES_PREVIOUS_VISIT = False
        self.visit_definition = VisitDefinition.objects.get(code='2000')
        next_appointment = Appointment.objects.create(
            registered_subject=self.registered_subject,
            appt_datetime=timezone.now(),
            visit_definition=self.visit_definition)
        test_visit = TestVisit.objects.create(
            appointment=next_appointment,
            report_datetime=timezone.now(),
            reason=SCHEDULED)
        self.assertIsNone(test_visit.previous_visit())

    def test_previous_visit_exists(self):
        TestVisit.REQUIRES_PREVIOUS_VISIT = False
        self.visit_definition = VisitDefinition.objects.get(code='2000')
        next_appointment = Appointment.objects.create(
            registered_subject=self.registered_subject,
            appt_datetime=timezone.now(),
            visit_definition=self.visit_definition)
        previous_visit = TestVisit.objects.create(
            appointment=self.appointment,
            report_datetime=timezone.now(),
            reason=SCHEDULED)
        test_visit = TestVisit.objects.create(
            appointment=next_appointment,
            report_datetime=timezone.now(),
            reason=SCHEDULED)
        self.assertEqual(test_visit.previous_visit(), previous_visit)

    def test_previous_visit(self):
        TestVisit.REQUIRES_PREVIOUS_VISIT = True
        self.visit_definition = VisitDefinition.objects.get(code='2000')
        next_appointment = Appointment.objects.create(
            registered_subject=self.registered_subject,
            appt_datetime=timezone.now(),
            visit_definition=self.visit_definition)
        previous_visit = TestVisit.objects.create(
            appointment=self.appointment,
            report_datetime=timezone.now(),
            reason=SCHEDULED)
        test_visit = TestVisit.objects.create(
            appointment=next_appointment,
            report_datetime=timezone.now(),
            reason=SCHEDULED)
        self.assertEqual(test_visit.previous_visit(), previous_visit)

    def test_visit_raises_if_no_previous(self):
        TestVisit.REQUIRES_PREVIOUS_VISIT = True
        self.visit_definition = VisitDefinition.objects.get(code='2000')
        next_appointment = Appointment.objects.create(
            registered_subject=self.registered_subject,
            appt_datetime=timezone.now(),
            visit_definition=self.visit_definition)
        self.assertRaises(
            PreviousVisitError,
            TestVisit.objects.create,
            appointment=next_appointment,
            report_datetime=timezone.now(),
            reason=SCHEDULED)

    def test_visit_not_raised_for_first_visit(self):
        TestVisit.REQUIRES_PREVIOUS_VISIT = True
        with self.assertRaises(PreviousVisitError):
            try:
                TestVisit.objects.create(
                    appointment=self.appointment,
                    report_datetime=timezone.now(),
                    reason=SCHEDULED)
            except:
                pass
            else:
                raise PreviousVisitError
