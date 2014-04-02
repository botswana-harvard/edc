from datetime import datetime
from collections import OrderedDict

from django.test import TestCase

from edc.lab.lab_profile.classes import site_lab_profiles
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.subject.appointment.models import Appointment
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.registration.models import RegisteredSubject
from edc.testing.classes import TestLabProfile
from edc.testing.classes import TestVisitSchedule, TestAppConfiguration
from edc.testing.models import TestModel, TestScheduledModel, TestConsentWithMixin
from edc.testing.tests.factories import TestModelFactory, TestScheduledModelFactory, TestConsentWithMixinFactory, TestVisitFactory
from edc.core.bhp_variables.models import StudySite

from ..classes import ExportAsCsv
from ..models import ExportHistory, ExportTransaction


class ExportAsCsvTests(TestCase):

    app_label = 'testing'

    def setUp(self):
        self.test_visit_factory = TestVisitFactory
        try:
            site_lab_profiles.register(TestLabProfile())
        except AlreadyRegisteredLabProfile:
            pass
        TestAppConfiguration()
        site_lab_tracker.autodiscover()
        TestVisitSchedule().rebuild()
        study_site = StudySite.objects.all()[0]
        subject_consent = TestConsentWithMixinFactory(study_site=study_site)
        self.registered_subject = RegisteredSubject.objects.get(subject_identifier=subject_consent.subject_identifier)
        self.consent = TestConsentWithMixin.objects.get(registered_subject=self.registered_subject)
        appointment = Appointment.objects.get(registered_subject=self.registered_subject)
        self.test_visit = TestVisitFactory(appointment=appointment)

    def test_field_names1(self):
        """Correctly sets field names based on the given model."""
        for i in range(0, 10):
            TestModelFactory()
        queryset = TestModel.objects.all()
        export_as_csv = ExportAsCsv(queryset, model=TestModel)
        export_as_csv.field_names.sort()
        field_names = [fld.name for fld in TestModel._meta.fields]
        field_names.sort()
        self.assertEqual(export_as_csv.field_names, field_names)

    def test_field_names2(self):
        """Extra fields are correctly updated to field names."""
        for i in range(0, 10):
            TestModelFactory()
        queryset = TestModel.objects.all()
        extra_fields = OrderedDict({'field 10': 'f10', 'field 20': 'f20'})
        export_as_csv = ExportAsCsv(queryset, model=TestModel, extra_fields=extra_fields)
        export_as_csv.field_names.sort()
        extra_field_names = []
        for header, field in extra_fields.iteritems():
            extra_field_names.append((header, field))
        field_names = [fld.name for fld in TestModel._meta.fields] + extra_field_names
        field_names.sort()
        self.assertEqual(export_as_csv.field_names, field_names)

    def test_field_names3(self):
        """Fields in 'fields' attribute are correctly updated to field names."""
        for i in range(0, 10):
            TestModelFactory()
        queryset = TestModel.objects.all()
        names = ['f10', 'f11']
        export_as_csv = ExportAsCsv(queryset, model=TestModel, fields=names)
        export_as_csv.field_names.sort()
        field_names = [fld.name for fld in TestModel._meta.fields] + names
        field_names.sort()
        self.assertEqual(export_as_csv.field_names, field_names)

    def test_field_names4(self):
        """Fields in 'exclude' attribute are correctly updated to field names."""
        for i in range(0, 10):
            TestModelFactory()
        queryset = TestModel.objects.all()
        names = ['f1', 'f2']
        export_as_csv = ExportAsCsv(queryset, model=TestModel, exclude=names)
        export_as_csv.field_names.sort()
        field_names = [fld.name for fld in TestModel._meta.fields if fld.name not in names]
        field_names.sort()
        self.assertEqual(export_as_csv.field_names, field_names)

    def test_get_field_name(self):
        """get a field name by name even if it is inside a tuple from extra fields."""
        for i in range(0, 10):
            TestModelFactory()
        queryset = TestModel.objects.all()
        names = ['f1', 'f2']
        extra_fields = OrderedDict({'field 10': 'f10', 'field 20': 'f20'})
        export_as_csv = ExportAsCsv(queryset, model=TestModel, exclude=names, extra_fields=extra_fields)
        export_as_csv.field_names.sort()
        field_names = [fld.name for fld in TestModel._meta.fields if fld.name not in names]
        field_names.sort()
        for field_name in export_as_csv.field_names:
            self.assertEqual(export_as_csv.get_field_name(field_name), field_name)

    def test_field_names_are_ordered(self):
        for i in range(0, 10):
            TestModelFactory()
        queryset = TestModel.objects.all()
        names = ['hostname_created', 'f1', 'subject_identifier']
        export_as_csv = ExportAsCsv(queryset, model=TestModel, fields=names, show_all_fields=False)
        export_as_csv.reorder_field_names()
        self.assertEqual(export_as_csv.field_names, ['subject_identifier', 'f1', 'hostname_created'])

    def test_header_row_is_ordered1(self):
        for i in range(0, 10):
            TestModelFactory()
        queryset = TestModel.objects.all()
        names = ['f1', 'hostname_created', 'f2', 'subject_identifier']
        export_as_csv = ExportAsCsv(queryset, model=TestModel, fields=names, show_all_fields=False)
        export_as_csv.reorder_field_names()
        self.assertEqual(export_as_csv.field_names, ['subject_identifier', 'f1', 'f2', 'hostname_created'])
        self.assertEqual(export_as_csv.header_row, ['subject_identifier', 'f1', 'f2', 'hostname_created'])

    def test_header_row_is_ordered2(self):
        for i in range(0, 10):
            TestModelFactory()
        queryset = TestModel.objects.all()
        names = ['f1', 'hostname_created', 'f2', 'report_datetime', 'subject_identifier']
        export_as_csv = ExportAsCsv(queryset, model=TestModel, fields=names, show_all_fields=False)
        export_as_csv.reorder_field_names()
        self.assertEqual(export_as_csv.field_names, ['subject_identifier', 'report_datetime', 'f1', 'f2', 'hostname_created'])
        self.assertEqual(export_as_csv.header_row, ['subject_identifier', 'report_datetime', 'f1', 'f2', 'hostname_created'])

    def test_header_row_is_ordered3(self):
        for i in range(0, 10):
            TestModelFactory()
        queryset = TestModel.objects.all()
        names = ['f1', 'hostname_created', 'report_datetime', 'report_datetime', 'f2', 'subject_identifier', 'f3']
        export_as_csv = ExportAsCsv(queryset, model=TestModel, fields=names, show_all_fields=False)
        export_as_csv.reorder_field_names()
        self.assertEqual(export_as_csv.field_names, ['subject_identifier', 'report_datetime', 'f1', 'f2', 'f3', 'hostname_created'])
        self.assertEqual(export_as_csv.header_row, ['subject_identifier', 'report_datetime', 'f1', 'f2', 'f3', 'hostname_created'])

    def test_getting_a_row1(self):
        for i in range(0, 10):
            TestModelFactory()
        queryset = TestModel.objects.all()
        names = ['f1', 'hostname_created', 'report_datetime', 'report_datetime', 'f2', 'subject_identifier', 'f3']
        export_as_csv = ExportAsCsv(queryset, model=TestModel, fields=names, show_all_fields=False)
        export_as_csv.reorder_field_names()
        export_as_csv.row_instance = TestModel.objects.all()[0]
        self.assertTrue(isinstance(export_as_csv.row, list))

    def test_getting_a_row2(self):
        """does it insert fields not directly on the model?"""
        TestScheduledModelFactory(test_visit=self.test_visit)
        queryset = TestScheduledModel.objects.all()
        names = ['f1', 'hostname_created', 'report_datetime', 'report_datetime', 'f2', 'subject_identifier', 'f3']
        export_as_csv = ExportAsCsv(queryset, model=TestScheduledModel, fields=names, show_all_fields=False)
        export_as_csv.reorder_field_names()
        export_as_csv.row_instance = TestModel.objects.all()[0]
        self.assertTrue(isinstance(export_as_csv.row, list))

    def test_getting_a_row3(self):
        """does it insert fields not directly on the model? for example subject_identifier"""
        TestScheduledModelFactory(test_visit=self.test_visit)
        queryset = TestScheduledModel.objects.all()
        names = ['f1', 'hostname_created', 'report_datetime', 'report_datetime', 'f2', 'test_visit__appointment__registered_subject__subject_identifier', 'f3']
        export_as_csv = ExportAsCsv(queryset, model=TestScheduledModel, fields=names, show_all_fields=False)
        export_as_csv.reorder_field_names()
        export_as_csv.row_instance = TestScheduledModel.objects.all()[0]
        self.assertNotIn('subject_identifier', export_as_csv.row)

    def test_getting_a_row4(self):
        """if it can't find the field, just puts in the field name"""
        TestScheduledModelFactory(test_visit=self.test_visit)
        queryset = TestScheduledModel.objects.all()
        names = ['f1', 'hostname_created', 'report_datetime', 'report_datetime', 'f2', 'test_visit__appointment__registered_subject__bad_dog', 'f3']
        export_as_csv = ExportAsCsv(queryset, model=TestScheduledModel, fields=names, show_all_fields=False)
        export_as_csv.reorder_field_names()
        export_as_csv.row_instance = TestScheduledModel.objects.all()[0]
        self.assertIn('bad_dog', export_as_csv.row)

    def test_getting_a_row5(self):
        """if it can't find the field, just puts in the field name"""
        TestScheduledModelFactory(test_visit=self.test_visit)
        queryset = TestScheduledModel.objects.all()
        fields = ['f1', 'hostname_created', 'report_datetime', 'report_datetime', 'f2', 'f3']
        extra_fields = OrderedDict({'subject_identifier': 'test_visit__appointment__registered_subject__subject_identifier'})
        export_as_csv = ExportAsCsv(queryset, model=TestScheduledModel, fields=fields, extra_fields=extra_fields, show_all_fields=False)
        export_as_csv.reorder_field_names()
        export_as_csv.row_instance = TestScheduledModel.objects.all()[0]
        self.assertNotIn('subject_identifier', export_as_csv.row)

    def test_writes_to_file1(self):
        """writes to file"""
        test_scheduled_model = TestScheduledModelFactory(test_visit=self.test_visit)
        queryset = TestScheduledModel.objects.all()
        self.assertEqual(queryset.count(), 1)
        fields = ['f1', 'hostname_created', 'report_datetime', 'report_datetime', 'f2', 'f3']
        extra_fields = OrderedDict({'subject_identifier': 'test_visit__appointment__registered_subject__subject_identifier'})
        export_as_csv = ExportAsCsv(queryset, model=TestScheduledModel, fields=fields, extra_fields=extra_fields, show_all_fields=False, track_history=True)
        self.assertEqual(export_as_csv.write_to_file(), export_as_csv.file_obj)

    def test_updates_history1(self):
        """on export, export_history is updated"""
        test_scheduled_model = TestScheduledModelFactory(test_visit=self.test_visit)
        queryset = TestScheduledModel.objects.all()
        fields = ['f1', 'hostname_created', 'report_datetime', 'report_datetime', 'f2', 'f3']
        extra_fields = OrderedDict({'subject_identifier': 'test_visit__appointment__registered_subject__subject_identifier'})
        export_as_csv = ExportAsCsv(queryset, model=TestScheduledModel, fields=fields, extra_fields=extra_fields, show_all_fields=False, track_history=True)
        export_as_csv.write_to_file()
        self.assertEqual(ExportHistory.objects.filter(instance_pk=test_scheduled_model.pk).count(), 1)

    def test_doesnt_update_history(self):
        """on export, export_history is updated"""
        TestScheduledModelFactory(test_visit=self.test_visit)
        queryset = TestScheduledModel.objects.all()
        fields = ['f1', 'hostname_created', 'report_datetime', 'report_datetime', 'f2', 'f3']
        extra_fields = OrderedDict({'subject_identifier': 'test_visit__appointment__registered_subject__subject_identifier'})
        export_as_csv = ExportAsCsv(queryset, model=TestScheduledModel, fields=fields, extra_fields=extra_fields, show_all_fields=False, track_history=False)
        export_as_csv.write_to_file()
        self.assertEqual(ExportHistory.objects.all().count(), 0)

    def test_model_manager_serializes1(self):
        """test manager serializes to export_transactions, count"""
        TestScheduledModelFactory(test_visit=self.test_visit)
        self.assertEqual(ExportTransaction.objects.all().count(), 1)

    def test_model_manager_serializes2(self):
        """test manager serializes to export_transactions, look for pk"""
        test_scheduled_model = TestScheduledModelFactory(test_visit=self.test_visit)
        self.assertEqual(ExportTransaction.objects.get(tx_pk=test_scheduled_model.pk).tx_pk, test_scheduled_model.pk)

    def test_model_manager_serializes_on_insert(self):
        """test manager serializes and change_type is 'I'"""
        test_scheduled_model = TestScheduledModelFactory(test_visit=self.test_visit)
        self.assertEqual(ExportTransaction.objects.get(tx_pk=test_scheduled_model.pk).change_type, 'I')

    def test_model_manager_serializes_on_update(self):
        """test manager serializes and change_type is 'U'"""
        test_scheduled_model = TestScheduledModelFactory(test_visit=self.test_visit)
        test_scheduled_model.f1 = 'XXX'
        test_scheduled_model.save()
        self.assertEqual(ExportTransaction.objects.get(tx_pk=test_scheduled_model.pk, change_type='U').change_type, 'U')

    def test_model_manager_serializes_on_delete(self):
        """test manager serializes and change_type is 'D'"""
        test_scheduled_model = TestScheduledModelFactory(test_visit=self.test_visit)
        pk = test_scheduled_model.pk
        test_scheduled_model.delete()
        self.assertTrue(ExportTransaction.objects.get(tx_pk=pk, change_type='D').change_type, 'D')
