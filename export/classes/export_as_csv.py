import csv
import datetime

from django.db.models.constants import LOOKUP_SEP
from django.http import HttpResponse


class ExportAsCsv(object):

    def __init__(self, queryset, model=None, modeladmin=None, fields=None, exclude=None, extra_fields=None, header=True, track_history=False):
        self._field_names = None
        self._modeladmin = modeladmin
        self._model = None
        self._file_obj = None
        self._header_row = None
        self._track_history = track_history
        self._queryset = queryset
        self.set_model(model)
        self.set_field_names_from_model()  # set initial field name list
        self._include_header = header  # writer to include a header row
        # adjustments
        self.append_field_names(fields)  # a list of names
        self.append_field_names(extra_fields)  # Extra fields is a list of dictionaries of [{'label': 'django_style__query_string'}, {}...].
        self.delete_field_names(exclude)  # a list of names

    def set_file_obj(self):
        self._file_obj = HttpResponse(mimetype='text/csv')
        self._file_obj['Content-Disposition'] = 'attachment; filename={filename}'.format(filename=self.get_export_filename())

    def get_file_obj(self):
        """Returns a file object for the writer."""
        return self._file_obj

    def write_to_file(self):
        """Writes the export file and returns the file object."""
        writer = csv.writer(self.get_file_obj())
        for obj in self.get_queryset():
            self.append_m2m_to_header_row(obj)
            if self.get_include_header():
                writer.writerow(self.get_header_row())
            writer.writerow(self.get_row())
            self.update_export_history(obj)
        return self.get_file_obj()

    def get_row(self, obj):
        """Returns a one row for the writer."""
        row = []
        for field in self.get_field_names():
            if field in self.get_queryset().model.__dict__:
                # is a field_attr for the queryset.model, append field object value to row
                row.append(unicode(getattr(obj, field)).encode("utf-8", "replace"))
            else:
                # is not a field attribute for this model, must be a django-style query_string
                # split on LOOKUP_SEP
                query_list = field.split(LOOKUP_SEP)
                # recurse to last field object to get value
                item = self.recurse_getattr(obj, query_list)
                # append to row
                row.append(unicode(item).encode("utf-8", "replace"))
        for m2m in obj._meta.many_to_many:
            values = self.get_m2m_value_delimiter().join([item.name.encode("utf-8", "replace") for item in getattr(obj, m2m.name).all()])
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

    def get_queryset(self):
        """Returns the queryset to be exported."""
        self._queryset

    def get_field_names(self):
        return self._field_names

    def set_field_names_from_model(self):
        """Sets field names by inspecting the model class for its field names."""
        self._field_names = [field.name for field in self.get_model()._meta.fields]
        self.set_header_row()

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
                    self.get_field_names().extend([fld for fld in append_fields.itervalues() if fld not in self._field_names])
                    self.get_header_row().extend([fld for fld in append_fields.itervalues() if fld not in self._field_names])
                else:
                    self.get_field_names().extend([fld for fld in append_fields if fld not in self._field_names])
                    self.get_header_row().extend([fld for fld in append_fields if fld not in self._field_names])

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

    def set_header_row(self):
        """Sets the header row to whatever :func:`get_field_names` returns."""
        self._header_row = self.get_field_names()

    def get_header_row(self):
        """Returns the header row."""
        return self._header_row

    def append_to_header_row(self, value):
        """Appends a name to the header row names list."""
        self.get_header_row.append(value)

    def append_m2m_to_header_row(self, obj):
        """Appends m2m field names which are not included in _meta.fields."""
        if not self._header_complete:
            for m2m in obj._meta.many_to_many:
                self.append_to_header_row(m2m.name)
            self._header_complete = True

    def get_field_delimiter(self):
        return ','

    def get_m2m_value_delimiter(self):
        """Returns the delimiter for m2m values (for fields with a list of values)."""
        return ';'

    def get_export_filename(self):
        """Returns the filename."""
        return '{0}.csv'.format(unicode(self.get_model()._meta).replace('.', '_'), datetime.datetime.now().strftime('%Y%m%d'))

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
                # DoesNotExist
                return '(none)'
        return getattr(obj, query_list[0])

    def update_export_history(self, obj):
        if self._track_history:
            self.get_model().export_history.update(obj)
