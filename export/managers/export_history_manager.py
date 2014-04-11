from datetime import datetime

from django.db import models
from django.core import serializers

from edc.core.crypto_fields.classes import FieldCryptor

from ..models import ExportTransaction


class ExportHistoryManager(models.Manager):

# see https://github.com/treyhunner/django-simple-history/ for some ideas to improve this
#     def __init__(self, model, instance=None):
#         super(ExportHistoryManager, self).__init__()
#         self.model = model
#         self.instance = instance
# 
#     def get_query_set(self):
#         if self.instance is None:
#             return super(ExportHistoryManager, self).get_query_set()
#         return super(ExportHistoryManager, self).get_query_set().filter(**{'instance_pk': self.instance.pk})

    def serialize_to_export_transaction(self, instance, change_type, using, encrypt=True):
        """Serialize this instance to the export transaction model if ready."""
        try:
            ready_to_export_transaction = instance.ready_to_export_transaction
        except AttributeError:
            ready_to_export_transaction = True
        if ready_to_export_transaction:
            if instance._meta.proxy_for_model:  # if this is a proxy model, get to the main model
                instance = instance._meta.proxy_for_model.objects.get(id=instance.id)
            json_tx = serializers.serialize("json", [instance, ], ensure_ascii=False, use_natural_keys=False)
            if encrypt:
                json_tx = FieldCryptor('aes', 'local').encrypt(json_tx)
            return ExportTransaction.objects.using(using).create(
                app_label=instance._meta.app_label,
                object_name=instance._meta.object_name,
                tx_pk=instance.id,
                export_change_type=change_type,
                exported=False,
                export_uuid=instance.export_uuid,
                status='new',
                tx=json_tx,
                timestamp=datetime.today().strftime('%Y%m%d%H%M%S%f'),
                )
