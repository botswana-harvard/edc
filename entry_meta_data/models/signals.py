import re

from django.db.models.signals import post_save, pre_delete, post_delete
from django.dispatch import receiver

from edc.subject.visit_tracking.models import BaseVisitTracking
from edc.subject.entry.classes import ScheduledEntry


@receiver(post_save, weak=False, dispatch_uid="entry_meta_data_on_post_save")
def entry_meta_data_on_post_save(sender, instance, raw, created, using, update_fields, **kwargs):
    if isinstance(instance, BaseVisitTracking):
        ScheduledEntry(instance.appointment, instance).add_or_update_for_visit()
    else:
        try:
            change_type = 'I'
            if not created:
                change_type = 'U'
            sender.entry_meta_data_manager.update_meta_data(instance, change_type, using=using)
        except AttributeError as e:
            if 'entry_meta_data_manager' in str(e):
                pass
            else:
                raise


@receiver(pre_delete, weak=False, dispatch_uid="entry_meta_data_on_pre_delete")
def entry_meta_data_on_pre_delete(sender, instance, using, **kwargs):
    try:
        sender.entry_meta_data_manager.update_meta_data(instance, 'D', using=using)
    except AttributeError as e:
        if 'entry_meta_data_manager' in str(e):
            pass
        else:
            raise


@receiver(post_delete, weak=False, dispatch_uid="entry_meta_data_on_post_delete")
def entry_meta_data_on_post_delete(sender, instance, using, **kwargs):
    """Delete metadata if the visit tracking instance is deleted."""
    if isinstance(instance, BaseVisitTracking):
        ScheduledEntry(instance.appointment, sender).delete_for_visit(instance)
