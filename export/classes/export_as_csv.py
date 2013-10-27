import csv
import datetime

from collections import OrderedDict

from django.db.models.constants import LOOKUP_SEP
from django.http import HttpResponse

from ..models import ExportHistory


class ExportAsCsv(object):

    def __init__(self, queryset, model=None, modeladmin=None, fields=None, exclude=None, extra_fields=None, header=True, track_history=False, show_all_fields=True):
        self._field_names = []
        self._modeladmin = modeladmin
        self._model = None
        self._file_obj = None
        self._header_row = None
        self._header_from_m2m_complete = False
        self._extra_fields = None
        self._track_history = track_history
        self._queryset = queryset
        self.set_model(model)
        if show_all_fields:
            self.set_field_names_from_model()  # set initial field name list
        self._include_header = header  # writer to include a header row
        self.append_field_names(fields)  # a list of names
        self.append_field_names(extra_fields)  # Extra fields is a list of dictionaries of [{'label': 'django_style__query_string'}, {}...].
        self.delete_field_names(exclude)  # a list of names
        self.set_export_filename()

    def get_queryset(self):
        """Returns the queryset to be exported."""
        return self._queryset

    def set_file_obj(self):
        self._file_obj = HttpResponse(mimetype='text/csv')
        self._file_obj['Content-Disposition'] = 'attachment; filename={filename}'.format(filename=self.get_export_filename())

    def get_file_obj(self):
        """Returns a file object for the writer."""
        return self._file_obj

    def write_to_file(self):
        """Writes the export file and returns the file object."""
        self.set_file_obj()
        writer = csv.writer(self.get_file_obj())
        self.reorder_field_names()
        self.set_header_row()
        for obj in self.get_queryset():
            self.append_m2m_to_header_row(obj)
            if self.get_include_header():
                writer.writerow(self.get_header_row())
            writer.writerow(self.get_row(obj))
            self.update_export_history(obj)
        return self.get_file_obj()

    def get_row_value_from_attr(self, obj, field_name):
        """Gets the row value from the model attr."""
        value = None
        value_error_placeholder = None
        try:
            value = getattr(obj, field_name)
            if value:
                value = unicode(value).encode("utf-8", "replace")
        except AttributeError:
            value_error_placeholder = field_name.split(LOOKUP_SEP)[-1]  # no harm in splitting even if usually nothing to split
        return value, value_error_placeholder

    def get_row_value_from_query_string(self, obj, field_name):
        """Gets the row value by following the query string to related instances."""
        value = None
        value_error_placeholder = None
        if self.get_extra_field(field_name) or self.get_field_name(field_name):
            try:
                query_string = self.get_extra_field(field_name) or self.get_field_name(field_name)
                query_list = query_string.split(LOOKUP_SEP)
                value, value_error_placeholder = self.recurse_getattr(obj, query_list)  # recurse to last relation to get value
                if value:
                    value = unicode(value).encode("utf-8", "replace")
            except AttributeError:
                value_error_placeholder = field_name.split(LOOKUP_SEP)[-1]
        return value, value_error_placeholder

    def get_row_values_from_m2m(self, obj):
        """Look for m2m fields and get the values and return as a delimited string of values."""
        values = None
        for m2m in obj._meta.many_to_many:
            values = self.get_m2m_value_delimiter().join([item.name.encode("utf-8", "replace") for item in getattr(obj, m2m.name).all()])
        return values

    def get_row(self, obj):
        """Returns a one row for the writer."""
        row = []
        value = None
        value_error_placeholder = None  # if error getting value, just show the field name
        for field_name in self.get_field_names():
            value, value_error_placeholder = self.get_row_value_from_attr(obj, field_name)
            if value_error_placeholder and LOOKUP_SEP in field_name:
                value, value_error_placeholder = self.get_row_value_from_query_string(obj, field_name)
            row.append(value_error_placeholder or value)
        values = self.get_row_values_from_m2m(obj)
        if values:
            row.append(values)
        return row

    def get_include_header(self):
        return self._include_header

    def get_modeladmin(self):
        return self._modeladmin

    def set_model(self, model=None):
        """Sets model to that from modeladmin or model."""
        if self.get_modeladmin():
            self._model = self.get_modeladmin().model
        else:
            self._model = model
        if not self._model:
            raise AttributeError('Attribute model may not be None.')

    def get_model(self):
        return self._model

    def set_field_names(self, value):
        """Sets the field names list."""
        self._field_names = list(OrderedDict.fromkeys(value))

    def update_field_names(self, value):
        """Updates the field_names list by either appending or extending."""
        if not self._field_names:
            self._field_names = []
        if isinstance(value, list):
            self._field_names.extend(value)
        else:
            self._field_names.append(value)
        self._field_names = list(OrderedDict.fromkeys(self._field_names))  # remove dups, preserve order

    def get_field_names(self):
        return self._field_names

    def get_field_name(self, field_name):
        """Returns the field name if it is in the list.

        Like this so it is similar to the dictionary get for extra fields."""
        return self._field_names[self._field_names.index(field_name)]

    def get_extra_fields(self):
        """Returns a dictionary of {<field_label>, <django_style__query_string>, ...}."""
        return self._extra_fields or {}

    def get_extra_field(self, key):
        return self.get_extra_fields().get(key, None)

    def update_extra_fields(self, dct):
        self.get_extra_fields().update(dct)

    def set_field_names_from_model(self):
        """Sets field names by inspecting the model class for its field names."""
        self.update_field_names([field.name for field in self.get_model()._meta.fields])

    def append_field_names(self, fields):
        """Appends field names to the list given a dictionary or list."""
        if fields:
            if isinstance(fields, list):
                append_fields = None
                for field in fields:
                    if isinstance(field, dict):
                        if not append_fields:
                            append_fields = {}
                        append_fields.update(field)
                    else:
                        if not append_fields:
                            append_fields = []
                        append_fields.append(field)
                if append_fields:
                    if isinstance(append_fields, dict):
                        # TODO: these are field names or references to field names (e.g subject_visit__appointment__appt_datetime)
                        # do these need to be verified?
                        self.update_field_names([fldname for fldname in append_fields.itervalues() if fldname not in self.get_field_names()])
                        self.update_extra_fields(append_fields)
                    else:
                        self.update_field_names([fldname for fldname in append_fields if fldname not in self.get_field_names()])

    def delete_field_names(self, fields):
        """Extra fields is a list of dictionaries of [{'label': 'query_string'}, {}...]."""
        if fields:
            for field_name in fields:
                # delete from field names
                try:
                    self.get_field_names().pop(self.get_field_names().index(field_name))
                except ValueError:
                    raise ValueError('Invalid field name in exclude. Got {0}'.format(field_name))
                # delete from header row
                try:
                    self.get_header_row().pop(self.get_header_row().index(field_name))
                except ValueError:
                    pass

    def reorder_field_names(self):
        """Reorder the field names so that subject_identifier is first and required fields are last."""
        # move subject_identifier to the top of the list
        name = None
        try:
            name = self.get_field_names().pop(self.get_field_names().index('subject_identifier'))
            self.get_field_names().insert(0, name)
        except ValueError:
            pass
        try:
            name = self.get_field_names().pop(self.get_field_names().index('report_datetime'))
            self.get_field_names().insert(1, name)
        except ValueError:
            pass
        # move required fields to the end of the list
        required_fields = []
        for name in ['hostname_created', 'hostname_modified', 'created', 'modified', 'user_created', 'user_modified', 'revision']:
            try:
                required_fields.append(self.get_field_names().pop(self.get_field_names().index(name)))
            except ValueError:
                pass
        self.get_field_names().extend(required_fields)

    def set_header_row(self):
        """Sets the header row to whatever :func:`get_field_names` returns."""
        self._header_row = [name.split(LOOKUP_SEP)[-1] for name in self.get_field_names()]

    def get_header_row(self):
        """Returns the header row."""
        return self._header_row or []

    def append_to_header_row(self, value):
        """Appends a name to the header row names list."""
        self.get_header_row().append(value)

    def append_m2m_to_header_row(self, obj):
        """Appends m2m field names which are not included in _meta.fields."""
        if not self._header_from_m2m_complete:
            for m2m in obj._meta.many_to_many:
                self.append_to_header_row(m2m.name)
            self._header_from_m2m_complete = True

    def get_field_delimiter(self):
        return ','

    def get_m2m_value_delimiter(self):
        """Returns the delimiter for m2m values (for fields with a list of values)."""
        return ';'

    def set_export_filename(self):
        self._export_filename = '{0}.csv'.format(unicode(self.get_model()._meta).replace('.', '_'), datetime.datetime.now().strftime('%Y%m%d'))

    def get_export_filename(self):
        """Returns the filename."""
        return self._export_filename

    def recurse_getattr(self, obj, query_list):
        """ Recurse on result of getattr() with a given query string as a list.

        The query_list is based on a django-style query string split on '__' into
        a list. For example 'field_attr__model_name__field_attr' split to
        ['field_attr', 'model_name', 'field_attr']
        """
        if len(query_list) > 1:
            try:
                return self.recurse_getattr(getattr(obj, query_list[0]), query_list[1:])
            except:
                return None, query_list[-1]
        return getattr(obj, query_list[0]), None

    def update_export_history(self, obj):
        if self._track_history:
            ExportHistory.objects.update()
