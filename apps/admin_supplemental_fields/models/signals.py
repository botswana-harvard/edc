from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from base.model.models import BaseModel

from .excluded_history import ExcludedHistory


# @receiver(post_save, weak=False, dispatch_uid='supplemental_fields_on_post_save')
# def supplemental_fields_on_post_save(sender, instance, **kwargs):
#     if isinstance(instance, (BaseModel)):
#         ExcludedHistory.objects.filter(model_pk=instance.pk).delete()

@receiver(post_delete, weak=False, dispatch_uid='supplemental_fields_on_post_delete')
def supplemental_fields_on_post_delete(sender, instance, **kwargs):
    if isinstance(instance, (BaseModel)):
        ExcludedHistory.objects.filter(model_pk=instance.pk).delete()
