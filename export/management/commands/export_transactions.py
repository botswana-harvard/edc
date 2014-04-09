import json

from django.core import serializers
from django.db.models import get_model
from django.core.management.base import BaseCommand, CommandError

from edc.core.crypto_fields.classes import FieldCryptor
from edc.export.models.export_transaction import ExportTransaction

from ...classes import ExportJsonAsCsv
from ...models import ExportPlan


class Command(BaseCommand):

    args = '<app_label>.<model_name>'
    help = 'Export transactions for a given app_label.model_name.'
    option_list = BaseCommand.option_list

    def handle(self, *args, **options):
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
            target_path=export_plan.target_path)
        export_json_as_csv.write_to_file()
        self.stdout.write('Successfully exported {0} transactions to file {1} for model {2}.{3}.'.format(tx_count, export_json_as_csv.export_filename, app_label, model_name))
