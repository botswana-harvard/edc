from django.db import models
from django.utils.translation import ugettext as _
from edc.base.model.validators import date_not_future, date_is_future
from edc.base.model.models import BaseUuidModel
from edc.choices.common import YES_NO
from edc.core.bhp_research_protocol.models import Site
from edc.core.bhp_research_protocol.models import Protocol


class SimpleConsent (BaseUuidModel):

    protocol = models.ForeignKey(Protocol)

    consent_site = models.ForeignKey(Site)

    consent_startdate = models.DateField("Consent date",
        validators=[
            date_not_future, ],
        )

    consent_enddate = models.DateField("Consent valid until",
        validators=[
            date_is_future, ],
        null=True,
        blank=True,
        )

    may_store_samples = models.CharField(
        verbose_name=_("Sample storage"),
        max_length=3,
        choices=YES_NO,
        help_text=_("Does the subject agree to have samples stored after the study has ended")
        )

    def get_absolute_url(self):
        return "/lab_patient/simpleconsent/%s/" % self.id

    def __unicode__(self):
        return "%s from %s to %s" % (self.protocol, self.consent_startdate, self.consent_enddate)

    class Meta:
        ordering = ["consent_startdate"]
        app_label = 'lab_patient'
        db_table = 'bhp_lab_registration_simpleconsent'
