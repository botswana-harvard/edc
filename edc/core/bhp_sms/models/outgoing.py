from django.db import models
from ..choices import OUTGOING_SMS_STATUS
from ..classes import BaseSms


class OutgoingSms(BaseSms):
    is_delivered = models.BooleanField(default=False)
    is_sent = models.BooleanField(default=False)
    status = models.CharField(
        max_length=20,
        choices=OUTGOING_SMS_STATUS
        )

    def __unicode__(self):
        return "%s -> %s" % (self.phone, self.text)

    class Meta:
        db_table = u'outgoing_sms'
        app_label = 'bhp_sms'
