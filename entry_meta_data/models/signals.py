from django.db.models.signals import post_save, pre_delete, post_delete
from django.dispatch import receiver

from edc.subject.visit_tracking.models import BaseVisitTracking
from edc.subject.entry.classes import ScheduledEntry


@receiver(post_save, weak=False, dispatch_uid="entry_meta_data_on_post_save")
def entry_meta_data_on_post_save(sender, instance, raw, created, using, update_fields, **kwargs):
    from ..managers import EntryMetaDataManager  # causes import error if outside
    if isinstance(instance, BaseVisitTracking):
        ScheduledEntry().add_or_update_for_visit(instance)
    for manager in sender._meta.concrete_managers:
        if isinstance(manager[2], EntryMetaDataManager):
            change_type = 'I'
            if not created:
                change_type = 'U'
            sender.entry_meta_data_manager.update_meta_data(instance, change_type, using=using)


@receiver(pre_delete, weak=False, dispatch_uid="entry_meta_data_on_pre_delete")
def entry_meta_data_on_pre_delete(sender, instance, using, **kwargs):
    from ..managers import EntryMetaDataManager  # causes import error if outside
    for manager in sender._meta.concrete_managers:
        if isinstance(manager[2], EntryMetaDataManager):
            sender.entry_meta_data_manager.update_meta_data(instance, 'D', using=using)


@receiver(post_delete, weak=False, dispatch_uid="entry_meta_data_on_post_delete")
def entry_meta_data_on_post_delete(sender, instance, using, **kwargs):
    """Delete metadata if the visit tracking instance is deleted."""
    if isinstance(instance, BaseVisitTracking):
        ScheduledEntry().delete_for_visit(instance)
