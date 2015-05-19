from django.db import models
from edc.base.model.models import BaseUuidModel


class BaseAppendix(BaseUuidModel):

    code = models.CharField(
        max_length=25,
        unique=True,
        )

    short_description = models.CharField(
        max_length=300,
        )

    full_description = models.TextField(
        max_length=600
        )

    class Meta:
        abstract = True