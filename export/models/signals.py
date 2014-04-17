from datetime import datetime
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from edc.export.models.export_receipts import ExportReceipts
from edc.export.models.export_transaction import ExportTransaction


@receiver(post_save, weak=False, dispatch_uid="export_to_transaction_on_post_save")
def export_to_transaction_on_post_save(sender, instance, raw, created, using, update_fields, **kwargs):
    from ..managers import ExportHistoryManager  # causes import error if outside
    for manager in sender._meta.concrete_managers:
        if isinstance(manager[2], ExportHistoryManager):
            change_type = 'I'
            if not created:
                change_type = 'U'
            sender.export_history.serialize_to_export_transaction(instance, change_type, using=using)


@receiver(pre_delete, weak=False, dispatch_uid="export_to_transaction_on_pre_delete")
def export_to_transaction_on_pre_delete(sender, instance, using, **kwargs):
    from ..managers import ExportHistoryManager  # causes import error if outside
    for manager in sender._meta.concrete_managers:
        if isinstance(manager[2], ExportHistoryManager):
            sender.export_history.serialize_to_export_transaction(instance, 'D', using=using)


@receiver(post_save, weak=False, dispatch_uid="export_receipt_on_post_save")
def export_receipt_on_post_save(sender, instance, raw, created, using, update_fields, **kwargs):
    if isinstance(instance, ExportReceipts):
        ExportTransaction.objects.filter(export_uuid=instance.export_uuid, received=False
                                         ).update(status='closed',
                                                  received=True,
                                                  received_datetime=datetime.today())

