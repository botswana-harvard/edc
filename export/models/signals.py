from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from ..managers import ExportHistoryManager


@receiver(post_save, weak=False, dispatch_uid="update_export_history_on_post_save")
def update_export_history_on_post_save(sender, instance, raw, created, using, update_fields, **kwargs):
    for manager in sender._meta.concrete_managers:
        if isinstance(manager[2], ExportHistoryManager):
            change_type = 'I'
            if not created:
                change_type = 'U'
            sender.export_history.serialize_to_export_transaction(instance, change_type, using=using)


@receiver(pre_delete, weak=False, dispatch_uid="update_export_history_on_post_save")
def update_export_history_on_pre_delete(sender, instance, using, **kwargs):
    for manager in sender._meta.concrete_managers:
        if isinstance(manager[2], ExportHistoryManager):
            sender.export_history.serialize_to_export_transaction(instance, 'D', using=using)
