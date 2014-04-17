import csv
import os

from datetime import datetime

from django.core.management.base import BaseCommand, CommandError

from ...models import ExportReceipt, ExportTransaction
from edc.export.models.export_plan import ExportPlan


class Command(BaseCommand):

    args = '<receipt filename>'
    help = 'Import a receipt file for recently exported transactions.'
    option_list = BaseCommand.option_list

    def handle(self, *args, **options):

        csvfile = args[0]
        app_label1, app_label2, object_name, timestamp = csvfile.split('_')
        app_label = app_label1 + '_' + app_label2
        header = []
        error_filename = '.'.join(['error'] + csvfile.split('.'))
        export_plan = ExportPlan.objects.get(app_label, object_name)
        target_path = export_plan.target_path
        with open(csvfile, 'r') as f, open(os.path.join(os.path.expanduser(target_path) or '', error_filename), 'w') as error_file:
            rows = csv.reader(f, delimiter='|')
            writer = csv.writer(error_file, delimiter='|')
            for row in rows:
                if not header:
                    header = row
                    continue
                export_uuid = row[row.index('export_UUID')]
                try:
                    export_transaction = ExportTransaction.objects.get(export_uuid=export_uuid)
                    ExportReceipt.objects.create(
                        export_uuid=export_uuid,
                        app_label=app_label,
                        object_name=object_name,
                        timestamp=timestamp,
                        received_datetime=datetime.today(),
                        tx_pk=export_transaction.tx_pk,
                        )
                except ExportTransaction.DoesNotExist:
                    writer.writerow(row)
