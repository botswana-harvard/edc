from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from edc.subject.visit_tracking.models import BaseVisitTracking
from edc.entry_meta_data.classes import ScheduledEntryMetaDataHelper, RequisitionMetaDataHelper


@receiver(post_save, weak=False, dispatch_uid="entry_meta_data_on_post_save")
def entry_meta_data_on_post_save(sender, instance, raw, created, using, update_fields, **kwargs):
    if isinstance(instance, BaseVisitTracking):
        scheduled_entry_helper = ScheduledEntryMetaDataHelper(instance.appointment, sender)
        scheduled_entry_helper.add_or_update_for_visit()
        requisition_meta_data_helper = RequisitionMetaDataHelper(instance.appointment, sender)
        requisition_meta_data_helper.add_or_update_for_visit()

    else:
        try:
            change_type = 'I'
            if not created:
                change_type = 'U'
            sender.entry_meta_data_manager.update_meta_data(instance, change_type, using=using)
            if sender.entry_meta_data_manager.instance:
                sender.entry_meta_data_manager.run_rule_groups()
        except AttributeError as e:
            if 'entry_meta_data_manager' in str(e):
                pass
            else:
                raise


@receiver(pre_delete, weak=False, dispatch_uid="entry_meta_data_on_pre_delete")
def entry_meta_data_on_pre_delete(sender, instance, using, **kwargs):
    """Delete metadata if the visit tracking instance is deleted."""
    if isinstance(instance, BaseVisitTracking):
        scheduled_entry_helper = ScheduledEntryMetaDataHelper(instance.appointment, sender)
        scheduled_entry_helper.delete_for_visit()
        requisition_meta_data_helper = RequisitionMetaDataHelper(instance.appointment, sender)
        requisition_meta_data_helper.delete_for_visit()
    else:
        try:
            sender.entry_meta_data_manager.update_meta_data(instance, 'D', using=using)
        except AttributeError as e:
            if 'entry_meta_data_manager' in str(e):
                pass
            else:
                raise
