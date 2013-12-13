from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .base_base_requisition import BaseBaseRequisition

@receiver(post_save, weak=False, dispatch_uid="requisition_identifier_as_uuid_on_post_save")
def requisition_identifier_as_uuid_on_post_save(sender, instance, **kwargs):
    if not kwargs.get('raw', False):
        if isinstance(instance, BaseBaseRequisition):
            instance.requisition_identifier_as_uuid_on_post_save(**kwargs)