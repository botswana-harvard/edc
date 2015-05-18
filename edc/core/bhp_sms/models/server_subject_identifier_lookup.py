from django.db import models
from ..classes import BaseSmsSubjectLookup
from ..models import IncomingSms


class ServerSubjectIdentifierLookup(BaseSmsSubjectLookup):
    incoming_sms = models.ForeignKey(IncomingSms,
        verbose_name='Request SMS',
        help_text="",
        )

    is_new_identifer = models.BooleanField(
        default=False,
        verbose_name="Was a new identifier created for this request"
        )

    is_sent = models.BooleanField(
        default=False,
        verbose_name="Was a new identifier created for this request"
        )

    def __unicode__(self):
        return "{0}->{}".format(self.incoming_sms.phone, )

    class Meta:
        app_label = "bhp_sms"
