from django.db import models
from bhp_consent.models import BaseConsentedUuidModel
from bhp_haart.choices import ARV_DRUG_LIST


class BaseHaartHistory(BaseConsentedUuidModel):
    """
    Does not include Dose Modification

    Base Class for recording HAART medications
    You need to at least add a 'id' field to this model.
    For example:

    ca008 = models.ForeignKey(Ca008)

    """

    arv_code = models.CharField(
        verbose_name="ARV Code",
        max_length=25,
        choices=ARV_DRUG_LIST,
        )

    date_start = models.DateField(
        verbose_name="Date Started",
        blank=True,
        null=True,
        )
    date_stop = models.DateField(
        verbose_name="Date Stopped",
        blank=True,
        null=True,
        )

    def natural_key(self):
        return (self.arv_code, self.date_start, self.date_stop)

    class Meta:
        abstract = True
        unique_together = ('arv_code', 'date_start', 'date_stop')
