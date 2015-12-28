from django.db import models

# from edc.device.sync.models import BaseSyncUuidModel
from edc_sync.models.sync_model_mixin import SyncModelMixin
from edc_base.model.models.base_uuid_model import BaseUuidModel


class NotificationPlan(SyncModelMixin, BaseUuidModel):

    name = models.CharField(max_length=50, unique=True)

    friendly_name = models.CharField(max_length=50)

    subject_format = models.TextField()

    body_format = models.TextField()

    recipient_list = models.TextField()

    cc_list = models.TextField()

    def is_serialized(self, serialize=True):
        return False

    class Meta:
        app_label = 'notification'
