from django.db import models
from edc_base.model.models import BaseUuidModel
from ..choices import SMS_TYPE


class BaseSms(BaseUuidModel):
    phone = models.CharField(max_length=20)
    text = models.CharField(max_length=255, blank=True)
    is_deleted = models.BooleanField(default=False)
    action = models.CharField(
                    max_length=250,
                    choices=SMS_TYPE
                    )

    class Meta:
        abstract = True
