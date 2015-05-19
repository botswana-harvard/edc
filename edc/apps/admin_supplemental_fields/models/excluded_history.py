from django.db import models

from edc.device.sync.models import BaseSyncUuidModel


class ExcludedHistory (BaseSyncUuidModel):

    app_label = models.CharField(
        max_length=50,
        )

    object_name = models.CharField(
        max_length=50,
        )

    model_pk = models.CharField(
        max_length=36,
        null=True,
        blank=True,
        )

    excluded_fields = models.TextField()

    group = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        )

    grouping_field = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        )

    grouping_pk = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        )

    objects = models.Manager()

    class Meta:
        app_label = 'admin_supplemental_fields'
