from datetime import datetime

from django.db import models
from django.core import serializers

from edc.core.crypto_fields.classes import FieldCryptor

from ..models import ExportHistory, ExportTransaction


class ExportHistoryManager(models.Manager):

    def get_queryset(self):
        """Returns a queryset with the export history of this model."""
        return ExportHistory.objects.all()

    def serialize_to_export_transaction(self, instance, change_type, using, encrypt=True):
        """Serialize this instance to the export transaction model."""
        if instance._meta.proxy_for_model:  # if this is a proxy model, get to the main model
            instance = instance._meta.proxy_for_model.objects.get(id=instance.id)
        json_tx = serializers.serialize("json", [instance, ], ensure_ascii=False, use_natural_keys=False)
        if encrypt:
            json_tx = FieldCryptor('aes', 'local').encrypt(json_tx)
        return ExportTransaction.objects.using(using).create(
            app_label=instance._meta.app_label,
            object_name=instance._meta.object_name,
            tx_pk=instance.id,
            change_type=change_type,
            status='new',
            tx=json_tx,
            timestamp=datetime.today().strftime('%Y%m%d%H%M%S%f'),
            )
