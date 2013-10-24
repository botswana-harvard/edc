from django.test import SimpleTestCase

from edc.testing.models import TestModel
from edc.testing.tests.factories import TestModelFactory

from ..classes import ExportAsCsv


class ExportAsCsvTests(SimpleTestCase):

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

    def test_field_(self):
        pass