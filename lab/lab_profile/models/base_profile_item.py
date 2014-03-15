from django.db import models

from edc.base.model.models import BaseUuidModel


class BaseProfileItem(BaseUuidModel):

    volume = models.DecimalField(verbose_name='Volume (ml)', max_digits=10, decimal_places=1, null=True)

    count = models.IntegerField(verbose_name='aliquots to create')

    def __unicode__(self):
        return self.aliquot_type

    class Meta:
        abstract = True
