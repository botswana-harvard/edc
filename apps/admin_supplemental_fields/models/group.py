from django.core.validators import RegexValidator
from django.db import models

from edc.base.model.models import BaseUuidModel


class Group(BaseUuidModel):

    name = models.CharField(
        max_length=5,
        validators=[RegexValidator('[A-Z]{1,5}')],
    )

    title = models.CharField(max_length=25)

    description = models.CharField(max_length=250)

    probability = models.FloatField()

    objects = models.Manager()

    class Meta:
        app_label = 'admin_supplemental_fields'
