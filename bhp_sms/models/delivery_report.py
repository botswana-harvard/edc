from django.db import models
from edc_core.bhp_base_model.models import BaseUuidModel
from ..choices import SMS_DELIVERY_REPORT
from ..models import OutgoingSms


class SmsDlr(BaseUuidModel):
    status = models.CharField(
                max_length=50,
                choices=SMS_DELIVERY_REPORT
            )
    sms = models.ForeignKey(OutgoingSms)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def recipient(self):
        return "%s" % (self.sms.phone)

    def __unicode__(self):
        return "%s (%s)" % (self.sms.phone, self.status)

    class Meta:
        db_table = u'sms_dlr'
        app_label = 'bhp_sms'
