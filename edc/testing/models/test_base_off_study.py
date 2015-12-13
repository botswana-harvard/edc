from edc_base.audit_trail import AuditTrail
from edc_offstudy.models import BaseOffStudy


class TestBaseOffStudy(BaseOffStudy):
    """ Test Off-Study."""

    history = AuditTrail()

    def __unicode__(self):
        return '{0} '.format(self.registered_subject)

    class Meta:
        app_label = 'testing'
