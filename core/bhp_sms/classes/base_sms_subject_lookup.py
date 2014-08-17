from django.db import models
from edc.base.model.models import BaseUuidModel


class BaseSmsSubjectLookup(BaseUuidModel):
    subject_identifier = models.CharField(
        verbose_name="Subject Identifier",
        max_length=36,
        null=True,
        blank=True,
        db_index=True,
        )

    token = models.CharField(
        verbose_name="Token/Pending ID",
        max_length=36,
        db_index=True,
        unique=True,
        )

    is_error = models.BooleanField(
        default=False,
        verbose_name="There was a problem retrieving the subject identifier"
        )

    class Meta:
        abstract = True
