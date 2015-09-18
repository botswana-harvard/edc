from django.db import models
try:
    from edc.device.sync.classes import BaseSyncModel as BaseUuidModel
except ImportError:
    from edc_base.model.models import BaseUuidModel
from edc_audit.audit_trail import AuditTrail


class Criteria(BaseUuidModel):

    subject_identifier = models.CharField(max_length=35)

    model_name = models.CharField(max_length=45)

    reference_datetime = models.DateTimeField()

    criteria = models.TextField(max_length=35)

    history = AuditTrail()

    objects = models.Manager()

    def __unicode__(self):
        return '{0} {1}'.format(self.subject_identifier, self.model_name)

    class Meta:
        app_label = 'bhp_eligibility'
