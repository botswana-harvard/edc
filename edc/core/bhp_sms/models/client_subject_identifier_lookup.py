from django.db import models
from ..classes import BaseSmsSubjectLookup
from ..models import OutgoingSms


class ClientSubjectIdentifierLookup(BaseSmsSubjectLookup):
    outgoing_sms = models.ForeignKey(OutgoingSms,
        verbose_name='Request SMS to the server',
        help_text="",
        )

    app_label = models.CharField(
        verbose_name="Application label",
        max_length=32,
        unique=True,
        )

    model_name = models.CharField(
        max_length=32,
        unique=True,
        )

    result_datetime = models.DateTimeField(
        null=True,
        blank=True
        )

    def __unicode__(self):
        return ""

    class Meta:
        app_label = "bhp_sms"
