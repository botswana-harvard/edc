from django.db.models.signals import post_delete
from django.dispatch import receiver

from edc.base.model.models import BaseModel

from .excluded_history import ExcludedHistory


@receiver(post_delete, weak=False, dispatch_uid='supplemental_fields_on_post_delete')
def supplemental_fields_on_post_delete(sender, instance, using, **kwargs):
    if isinstance(instance, (BaseModel)):
        ExcludedHistory.objects.using(using).filter(model_pk=instance.pk).delete()