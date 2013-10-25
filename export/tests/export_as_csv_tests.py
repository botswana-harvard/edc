from datetime import datetime

from django.test import TestCase

from edc.core.bhp_content_type_map.classes import ContentTypeMapHelper
from edc.core.bhp_content_type_map.models import ContentTypeMap
from edc.core.bhp_variables.tests.factories import StudySpecificFactory, StudySiteFactory
from edc.subject.appointment.models import Appointment
from edc.subject.appointment.tests.factories import ConfigurationFactory
from edc.subject.consent.tests.factories import ConsentCatalogueFactory
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.registration.models import RegisteredSubject
from edc.subject.registration.tests.factories import RegisteredSubjectFactory
from edc.subject.visit_schedule.tests.factories import MembershipFormFactory, ScheduleGroupFactory, VisitDefinitionFactory
from edc.testing.models import TestModel, TestScheduledModel
from edc.testing.tests.factories import TestModelFactory, TestScheduledModelFactory, TestVisitFactory, TestConsentFactory

from ..classes import ExportAsCsv


class ExportAsCsvTests(TestCase):

    app_label = 'testing'

    def setUp(self):
        site_lab_tracker.autodiscover()
        study_specific = StudySpecificFactory()
        StudySiteFactory()
        ConfigurationFactory()
        content_type_map_helper = ContentTypeMapHelper()
        content_type_map_helper.populate()
        content_type_map_helper.sync()
        content_type_map = ContentTypeMap.objects.get(content_type__model='SubjectConsent'.lower())
        ConsentCatalogueFactory(
            name=self.app_label,
            consent_type='study',
            content_type_map=content_type_map,
            version=1,
            start_datetime=study_specific.study_start_datetime,
            end_datetime=datetime(datetime.today().year + 5, 1, 1),
            add_for_app=self.app_label)
        membership_form = MembershipFormFactory(content_type_map=content_type_map)
        schedule_group = ScheduleGroupFactory(membership_form=membership_form, group_name='survey', grouping_key='SURVEY')
        visit_tracking_content_type_map = ContentTypeMap.objects.get(content_type__model='subjectvisit')
        visit_definition = VisitDefinitionFactory(code='T0', title='T0', grouping='subject', visit_tracking_content_type_map=visit_tracking_content_type_map)
        visit_definition.schedule_group.add(schedule_group)
        subject_consent = TestConsentFactory()
        print subject_consent.subject_identifier
        self.registered_subject = RegisteredSubject.objects.get(subject_identifier=subject_consent.subject_identifier)
        appointment = Appointment.objects.get(registered_subject=self.registered_subject)
        self.test_visit = TestVisitFactory(appointment=appointment)

    def test_field_names1(self):
        """Correctly sets field names based on the given model."""
        for i in range(0, 10):
            TestModelFactory()
        queryset = TestModel.objects.all()
        export_as_csv = ExportAsCsv(queryset, model=TestModel)
        export_as_csv.get_field_names().sort()
        field_names = [fld.name for fld in TestModel._meta.fields]
        field_names.sort()
        self.assertEqual(export_as_csv.get_field_names(), field_names)

    def test_field_names2(self):
        """Extra fields are correctly updated to field names."""
        for i in range(0, 10):
            TestModelFactory()
        queryset = TestModel.objects.all()
        extra_fields = [{'field 10': 'f10'}, {'field 20': 'f20'}]
        export_as_csv = ExportAsCsv(queryset, model=TestModel, extra_fields=extra_fields)
        export_as_csv.get_field_names().sort()
        extra_field_names = []
        for dct in extra_fields:
            for value in dct.itervalues():
                extra_field_names.append(value)
        field_names = [fld.name for fld in TestModel._meta.fields] + extra_field_names
        field_names.sort()
        self.assertEqual(export_as_csv.get_field_names(), field_names)

    def test_field_names3(self):
        """Fields in 'fields' attribute are correctly updated to field names."""
        for i in range(0, 10):
            TestModelFactory()
        queryset = TestModel.objects.all()
        names = ['f10', 'f11']
        export_as_csv = ExportAsCsv(queryset, model=TestModel, fields=names)
        export_as_csv.get_field_names().sort()
        field_names = [fld.name for fld in TestModel._meta.fields] + names
        field_names.sort()
        self.assertEqual(export_as_csv.get_field_names(), field_names)

    def test_field_names4(self):
        """Fields in 'exclude' attribute are correctly updated to field names."""
        for i in range(0, 10):
            TestModelFactory()
        queryset = TestModel.objects.all()
        names = ['f1', 'f2']
        export_as_csv = ExportAsCsv(queryset, model=TestModel, exclude=names)
        export_as_csv.get_field_names().sort()
        field_names = [fld.name for fld in TestModel._meta.fields if fld.name not in names]
        field_names.sort()
        self.assertEqual(export_as_csv.get_field_names(), field_names)

    def test_field_names_are_ordered(self):
        for i in range(0, 10):
            TestModelFactory()
        queryset = TestModel.objects.all()
        names = ['hostname_created', 'f1', 'subject_identifier']
        export_as_csv = ExportAsCsv(queryset, model=TestModel, fields=names, show_all_fields=False)
        export_as_csv.reorder_field_names()
        self.assertEqual(export_as_csv.get_field_names(), ['subject_identifier', 'f1', 'hostname_created'])

    def test_header_row_is_ordered1(self):
        for i in range(0, 10):
            TestModelFactory()
        queryset = TestModel.objects.all()
        names = ['f1', 'hostname_created', 'f2', 'subject_identifier']
        export_as_csv = ExportAsCsv(queryset, model=TestModel, fields=names, show_all_fields=False)
        export_as_csv.reorder_field_names()
        export_as_csv.set_header_row()
        self.assertEqual(export_as_csv.get_field_names(), ['subject_identifier', 'f1', 'f2', 'hostname_created'])
        self.assertEqual(export_as_csv.get_header_row(), ['subject_identifier', 'f1', 'f2', 'hostname_created'])

    def test_header_row_is_ordered2(self):
        for i in range(0, 10):
            TestModelFactory()
        queryset = TestModel.objects.all()
        names = ['f1', 'hostname_created', 'f2', 'report_datetime', 'subject_identifier']
        export_as_csv = ExportAsCsv(queryset, model=TestModel, fields=names, show_all_fields=False)
        export_as_csv.reorder_field_names()
        export_as_csv.set_header_row()
        self.assertEqual(export_as_csv.get_field_names(), ['subject_identifier', 'report_datetime', 'f1', 'f2', 'hostname_created'])
        self.assertEqual(export_as_csv.get_header_row(), ['subject_identifier', 'report_datetime', 'f1', 'f2', 'hostname_created'])

    def test_header_row_is_ordered3(self):
        for i in range(0, 10):
            TestModelFactory()
        queryset = TestModel.objects.all()
        names = ['f1', 'hostname_created', 'report_datetime', 'report_datetime', 'f2', 'subject_identifier', 'f3']
        export_as_csv = ExportAsCsv(queryset, model=TestModel, fields=names, show_all_fields=False)
        export_as_csv.reorder_field_names()
        export_as_csv.set_header_row()
        self.assertEqual(export_as_csv.get_field_names(), ['subject_identifier', 'report_datetime', 'f1', 'f2', 'f3', 'hostname_created'])
        self.assertEqual(export_as_csv.get_header_row(), ['subject_identifier', 'report_datetime', 'f1', 'f2', 'f3', 'hostname_created'])

    def test_getting_a_row1(self):
        for i in range(0, 10):
            TestModelFactory()
        queryset = TestModel.objects.all()
        names = ['f1', 'hostname_created', 'report_datetime', 'report_datetime', 'f2', 'subject_identifier', 'f3']
        export_as_csv = ExportAsCsv(queryset, model=TestModel, fields=names, show_all_fields=False)
        export_as_csv.reorder_field_names()
        export_as_csv.set_header_row()
        obj = TestModel.objects.all()[0]
        self.assertTrue(isinstance(export_as_csv.get_row(obj), list))

    def test_getting_a_row2(self):
        """does it insert fields not directly on the model?"""
        TestScheduledModelFactory(test_visit=self.test_visit)
        queryset = TestScheduledModel.objects.all()
        names = ['f1', 'hostname_created', 'report_datetime', 'report_datetime', 'f2', 'subject_identifier', 'f3']
        export_as_csv = ExportAsCsv(queryset, model=TestScheduledModel, fields=names, show_all_fields=False)
        export_as_csv.reorder_field_names()
        export_as_csv.set_header_row()
        obj = TestScheduledModel.objects.all()[0]
        self.assertTrue(isinstance(export_as_csv.get_row(obj), list))
