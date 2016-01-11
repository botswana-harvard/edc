from django.db import models

from edc_base.model.models import BaseModel


class BaseCodeList (BaseModel):

    code = models.CharField(
        verbose_name="Code",
        max_length=15,
        unique=True)

    short_name = models.CharField(
        verbose_name="Name",
        max_length=35)

    long_name = models.CharField(
        verbose_name="Long Name",
        max_length=255,
        blank=True)

    def __unicode__(self):
        return "%s" % (self.short_name)

    class Meta:
        abstract = True
