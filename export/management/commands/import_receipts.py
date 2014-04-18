import csv
import os

from datetime import datetime

from django.core.management.base import BaseCommand, CommandError

from ...models import ExportReceipt, ExportTransaction, ExportPlan


class Command(BaseCommand):

    args = '<receipt filename>'
    help = 'Import a receipt file for recently exported transactions.'
    option_list = BaseCommand.option_list

    def handle(self, *args, **options):

        try:
            ack_filename = args[0]
        except IndexError:
            raise CommandError('Usage: import_receipts <receipt filename>')
        _, app_label1, app_label2, object_name, timestamp = ack_filename.split('_')
        app_label = app_label1 + '_' + app_label2
        timestamp, extension = timestamp.split('.')
        header = []
        rejects = False
        error_filename = '_'.join(['error', app_label1, app_label2, object_name, timestamp]) + '.' + extension
        export_plan = ExportPlan.objects.get(app_label=app_label, object_name=object_name)
        target_path = export_plan.target_path
        print 'reading file...'
        with open(ack_filename, 'r') as f, open(os.path.join(os.path.expanduser(target_path) or '', error_filename), 'w') as error_file:
            rows = csv.reader(f, delimiter='|')
            writer = csv.writer(error_file, delimiter='|')
            for row in rows:
                if not header:
                    header = row
                    continue
                export_uuid = row[header.index('export_UUID')]
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
                    export_transaction.status = 'closed'
                    export_transaction.received = True
                    export_transaction.received_datetime = datetime.today()
                    export_transaction.save()
                    print '  accepted: ' + export_uuid

                except ExportTransaction.DoesNotExist:
                    rejects = True
                    writer.writerow(row)
                    print '  rejected: ' + export_uuid
        if rejects:
            print 'Some receipts were rejected.'
            print 'See file {0} in {1}'.format(error_filename, os.path.join(os.path.expanduser(target_path)))
        else:
            print 'Success'
