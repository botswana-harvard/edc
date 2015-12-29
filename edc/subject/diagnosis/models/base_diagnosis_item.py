from django.db import models

from ..choices import STATUS, METHOD

from .base_base_diagnosis_item import BaseBaseDiagnosisItem
from .diagnosis_code import DiagnosisCode
from .diagnosis_organism import DiagnosisOrganism
from .diagnosis_site import DiagnosisSite


class BaseDiagnosisItem(BaseBaseDiagnosisItem):

    code = models.ForeignKey(DiagnosisCode)

    code_specify = models.CharField(
        verbose_name='Specify',
        max_length=50,
        null=True,
        blank=True)

    method = models.CharField(
        max_length=10,
        choices=METHOD)

    organism = models.ForeignKey(DiagnosisOrganism)

    site = models.ForeignKey(DiagnosisSite)

    status = models.CharField(
        max_length=10,
        choices=STATUS)

    resolution_date = models.DateField()

    class Meta:
        abstract = True
