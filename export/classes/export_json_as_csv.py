import csv
import os

from datetime import datetime

from .base_export import BaseExport


class ExportJsonAsCsv(BaseExport):

    def __init__(self, queryset, model=None, modeladmin=None, fields=None, exclude=None, extra_fields=None,
                 header=True, track_history=False, show_all_fields=True, delimiter=None, encrypt=True, strip=False,
                 target_path=None):
        self._row_instance = None
        self.export_transaction = None
        self.target_path = target_path
        super(ExportJsonAsCsv, self).__init__(queryset, model, modeladmin, fields, exclude, extra_fields, header,
                                              track_history, show_all_fields, delimiter, encrypt, strip)

    @property
    def row_instance(self):
        return self._row_instance

    @row_instance.setter
    def row_instance(self, row_instance):
        self._row_instance = row_instance
        if row_instance:
            self._row_instance.export_change_type, self._row_instance.export_datetime = (self._row_instance.export_transaction.export_change_type, datetime.today())

    def write_to_file(self):
        """Writes the export file and returns the file object."""
        with open(os.path.join(os.path.expanduser(self.target_path) or '', self.export_filename), 'w') as f:
            writer = csv.writer(f, delimiter=self.delimiter)
            if self.include_header_row:
                writer.writerow(self.header_row)
            for self.row_instance in self.queryset:
                writer.writerow(self.row)
                self.update_export_history(self.row_instance)

    def update_export_history(self, row_instance=None):
        self.row_instance.export_transaction.exported_datetime = self.row_instance.export_datetime
        self.row_instance.export_transaction.status = 'sent'
        self.row_instance.export_transaction.save()
