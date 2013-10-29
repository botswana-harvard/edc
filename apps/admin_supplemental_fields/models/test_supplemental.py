# from django.core.validators import RegexValidator
from django.db import models

from edc.base.model.models import BaseUuidModel


class TestSupplemental(BaseUuidModel):

    f1 = models.CharField(max_length=5, null=True, blank=True)
    f2 = models.CharField(max_length=5, null=True, blank=True)
    f3 = models.CharField(max_length=5, null=True, blank=True)
    f4 = models.CharField(max_length=5, null=True, blank=True)
    f5 = models.CharField(max_length=5, null=True, blank=True)

    objects = models.Manager()

    class Meta:
        app_label = 'admin_supplemental_fields'
