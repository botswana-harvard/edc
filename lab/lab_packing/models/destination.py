from collections import namedtuple

from django.db import models

from edc.audit.audit_trail import AuditTrail
from edc.device.sync.models import BaseSyncUuidModel

DestinationTuple = namedtuple('DestinationTuple', 'code name address tel email')


class Destination(BaseSyncUuidModel):

    code = models.CharField(
        verbose_name='Code',
        max_length=25,
        unique=True,
        )
    name = models.CharField(
        verbose_name='Name',
        max_length=50,
        )
    address = models.TextField(
        verbose_name='Address',
        max_length=250,
        )
    tel = models.CharField(
        verbose_name='Telephone',
        max_length=50,
        )
    email = models.CharField(
        verbose_name='Email',
        max_length=25,
        )

    history = AuditTrail()

    def __unicode__(self):
        return self.code

    def natural_key(self):
        return (self.code, )

    class Meta:
        app_label = 'lab_packing'