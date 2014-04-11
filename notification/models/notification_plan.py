from django.db import models

from edc.device.sync.models import BaseSyncUuidModel


class NotificationPlan(BaseSyncUuidModel):

    name = models.CharField(max_length=50, unique=True)

    friendly_name = models.CharField(max_length=50)

    subject_format = models.TextField()

    body_format = models.TextField()

    recipient_list = models.TextField()

    cc_list = models.TextField()

    class Meta:
        app_label = 'notification'
