from django.db import models
from edc.subject.consent.models import BaseConsentedUuidModel
from edc.choices import YES_NO
from ..choices import GRADE


class BaseBaseDiagnosisItem(BaseConsentedUuidModel):

    grade = models.CharField(
        max_length=10,
        choices=GRADE
        )

    onset_date = models.DateField(null=True, blank=False)

    is_eae_required = models.CharField(
        verbose_name='Require EAE report?',
        max_length=10,
        choices=YES_NO,
        )

    eae_reference = models.CharField(
        verbose_name='EAE Ref',
        max_length=15,
        null=True,
        blank=True,
        )

    class Meta:
        abstract = True
