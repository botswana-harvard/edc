from edc.audit.audit_trail import AuditTrail
from edc.subject.off_study.models import BaseOffStudy


class TestBaseOffStudy(BaseOffStudy):
    """ Test Off-Study."""

    history = AuditTrail()

    def __unicode__(self):
        return '{0} '.format(self.registered_subject)

    class Meta:
        app_label = "bhp_base_test"
