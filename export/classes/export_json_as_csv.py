import csv
import os

from .base_export import BaseExport


class ExportJsonAsCsv(BaseExport):

    def __init__(self, queryset, model=None, modeladmin=None, fields=None, exclude=None, extra_fields=None,
                 header=True, track_history=False, show_all_fields=True, delimiter=None, encrypt=True, strip=False,
                 target_path=None, notification_plan_name=None, export_datetime=None):
        self._row_instance = None
        self.export_transaction = None
        self.target_path = target_path
        self.export_datetime = export_datetime
        super(ExportJsonAsCsv, self).__init__(queryset, model, modeladmin, fields, exclude, extra_fields, header,
                                              track_history, show_all_fields, delimiter, encrypt, strip, notification_plan_name, export_datetime)

    @property
    def row_instance(self):
        return self._row_instance

    @row_instance.setter
    def row_instance(self, row_instance):
        self._row_instance = row_instance
        if row_instance:
            self._row_instance.export_change_type, self._row_instance.exported_datetime = (self._row_instance.export_transaction.export_change_type, self.export_datetime)

    def write_to_file(self):
        """Writes the export file and returns the file object."""
        exported_pk_list = []
        export_uuid_list = []
        export_file_contents = []
        with open(os.path.join(os.path.expanduser(self.target_path) or '', self.export_filename), 'w') as f:
            writer = csv.writer(f, delimiter=self.delimiter)
            if self.include_header_row:
                writer.writerow(self.header_row)
                export_file_contents.append(self.header_row)
            for self.row_instance in self.queryset:
                writer.writerow(self.row)
                export_file_contents.append(self.row)
                self.update_export_transaction(self.row_instance)
                exported_pk_list.append(self.row_instance.pk)
                export_uuid_list.append(self.row_instance.export_uuid)
        if self.track_history:
            self.update_export_history(exported_pk_list, export_uuid_list, export_file_contents)

    def update_export_transaction(self, row_instance=None):
        self.row_instance.export_transaction.exported_datetime = self.export_datetime
        self.row_instance.export_transaction.status = 'exported'
        self.row_instance.export_transaction.save()
