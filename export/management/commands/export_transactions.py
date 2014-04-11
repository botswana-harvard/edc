import json

from datetime import datetime

from django.core import serializers
from django.db.models import get_model
from django.core.management.base import BaseCommand, CommandError

from edc.core.crypto_fields.classes import FieldCryptor
from edc.export.models.export_transaction import ExportTransaction
from edc.notification.models import Notification, NotificationPlan

from ...classes import ExportJsonAsCsv
from ...models import ExportPlan
from django.contrib.webdesign.lorem_ipsum import sentence


class Command(BaseCommand):

    args = '<app_label>.<model_name>'
    help = 'Export transactions for a given app_label.model_name.'
    option_list = BaseCommand.option_list

    def handle(self, *args, **options):
        export_json_as_csv = None
        export_datetime = None
        export_filename = None
        export_plan = None
        exit_status = (1, 'Failed')
        try:
            json_decoder = json.decoder.JSONDecoder()
            app_label, model_name = args[0].split('.')
            try:
                model = get_model(app_label, model_name)
                if not model:
                    raise CommandError()
            except CommandError:
                raise CommandError('Method get_model returned None for {0}.{1}'.format(app_label, model_name))
            export_plan = ExportPlan.objects.get(app_label=model._meta.app_label, object_name=model._meta.object_name)
            export_transactions = ExportTransaction.objects.filter(app_label=model._meta.app_label, object_name=model._meta.object_name).exclude(status__in=['sent', 'cancelled', 'exported'], )
            tx_count = export_transactions.count()
            transactions = []
            for export_transaction in export_transactions:
                for obj in serializers.deserialize("json", FieldCryptor('aes', 'local').decrypt(export_transaction.tx)):
                    obj.object.export_transaction = export_transaction
                    transactions.append(obj.object)
            export_datetime = datetime.today()
            export_json_as_csv = ExportJsonAsCsv(
                transactions,
                model=model,
                fields=json_decoder.decode(export_plan.fields),
                exclude=json_decoder.decode(export_plan.exclude),
                extra_fields=json_decoder.decode(export_plan.extra_fields),
                header=export_plan.header,
                track_history=export_plan.track_history,
                show_all_fields=export_plan.show_all_fields,
                delimiter=export_plan.delimiter,
                encrypt=export_plan.encrypt,
                strip=export_plan.strip,
                target_path=export_plan.target_path,
                notification_plan_name=export_plan.notification_plan_name,
                export_datetime=export_datetime)
            export_json_as_csv.write_to_file()
            export_filename = export_json_as_csv.export_filename
        except Exception as e:
            exit_status = (1, 'Error exporting transactions for model {0}.{1}. Got "{2}"'.format(app_label, model_name, e))
        else:
            exit_status = (0, 'Successfully exported {0} transactions to file {1} for {2}.{3}.'.format(tx_count, export_json_as_csv.export_filename, app_label, model_name))
        self.stdout.write(exit_status[1])
        if export_json_as_csv:
            export_json_as_csv.export_history.exit_status = exit_status[0]
            export_json_as_csv.export_history.exit_message = exit_status[1]
            export_json_as_csv.export_history.export_datetime = export_datetime
            export_json_as_csv.export_history.save()
        if export_plan.notification_plan_name:
            notification_plan = NotificationPlan.objects.get(name=export_plan.notification_plan_name)
            exit_status_word = 'Success' if (exit_status[0] == 0) else 'Failed'
            Notification.objects.create(
                notification_datetime=export_datetime,
                notification_plan_name=notification_plan.name,
                subject=notification_plan.subject_format.format(exit_status=exit_status_word, timestamp=export_datetime.strftime('%Y-%m-%d %H:%M:%S'), ),
                body=notification_plan.body_format.format(
                    notification_plan_name=notification_plan.friendly_name,
                    exit_status=exit_status_word,
                    exit_status_message=exit_status[1],
                    file_name=export_filename,
                    tx_count=len(transactions),
                    export_datetime=export_datetime.strftime('%d %B %Y %H:%M')),
                recipient_list=notification_plan.recipient_list,
                cc_list=notification_plan.cc_list,
                )
