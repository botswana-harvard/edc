from django.db import models
from ..classes import BaseSms


class IncomingSms(BaseSms):

    is_rejected = models.BooleanField(default=False)
    is_error = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s -> %s" % (self.phone, self.text)

    class Meta:
        db_table = u'incoming_sms'
        app_label = 'bhp_sms'
