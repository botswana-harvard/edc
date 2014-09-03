import socket

from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

from ..classes import SerializeToTransaction

from .base_sync_uuid_model import BaseSyncUuidModel
from .incoming_transaction import IncomingTransaction


@receiver(post_save, weak=False, dispatch_uid="deserialize_to_inspector_on_post_save")
def deserialize_to_inspector_on_post_save(sender, instance, raw, created, using, **kwargs):
    if not raw:
        try:
            # method only exists on MiddleManTransaction
            instance.deserialize_to_inspector_on_post_save(instance, raw, created, using, **kwargs)
        except AttributeError:
            pass


@receiver(m2m_changed, weak=False, dispatch_uid='serialize_m2m_on_save')
def serialize_m2m_on_save(sender, action, instance, using, **kwargs):
    """ Part of the serialize transaction process that ensures m2m are
    serialized correctly.
    """
    if action == 'post_add':
        if isinstance(instance, BaseSyncUuidModel):
            if instance.is_serialized() and not instance._meta.proxy:
                serialize_to_transaction = SerializeToTransaction()
                # default raw to False, created to True
                # TODO: serialize is skipped if raw is True, how should raw
                # affect serialization of m2m?
                # https://docs.djangoproject.com/en/dev/ref/signals/#m2m-changed
                raw = False
                created = True
                serialize_to_transaction.serialize(sender, instance, raw, created, using, **kwargs)


@receiver(post_save, weak=False, dispatch_uid='serialize_on_save')
def serialize_on_save(sender, instance, raw, created, using, **kwargs):
    """ Serialize the model instance to the outgoing transaction
    model for consumption by another application.
    """
    if not raw:
        if isinstance(instance, BaseSyncUuidModel):
            hostname = socket.gethostname()
            if (instance.hostname_created == hostname and not instance.hostname_modified) or (instance.hostname_modified == hostname):
                if instance.is_serialized() and not instance._meta.proxy:
                    serialize_to_transaction = SerializeToTransaction()
                    serialize_to_transaction.serialize(sender, instance, raw, created, using, **kwargs)


@receiver(post_save, sender=IncomingTransaction, dispatch_uid="deserialize_on_post_save")
def deserialize_on_post_save(sender, instance, raw, created, using, **kwargs):
    pass
    """ Callback to deserialize an incoming transaction.

    as long as the transaction is not consumed or in error"""
