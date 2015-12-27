from django.db import models

from edc_base.model.models import BaseUuidModel
from edc_sync.models import SyncModelMixin


class DefaultValueLog(SyncModelMixin, BaseUuidModel):

    subject_identifier = models.CharField(max_length=50)
    subject_type = models.CharField(max_length=25, null=True)
    group_name = models.CharField(max_length=50)
    value_datetime = models.DateTimeField(null=True)
    value = models.CharField(max_length=50, null=True, blank=True)
    error_message = models.TextField(max_length=500, null=True)
    objects = models.Manager()

    class Meta:
        app_label = 'lab_tracker'
