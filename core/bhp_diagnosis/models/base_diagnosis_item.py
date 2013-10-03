from django.db import models
from bhp_diagnosis.choices import STATUS, METHOD
from code import Code
from site import Site
from organism import Organism
from base_base_diagnosis_item import BaseBaseDiagnosisItem


class BaseDiagnosisItem(BaseBaseDiagnosisItem):

    code = models.ForeignKey(Code)

    code_specify = models.CharField(
        verbose_name='Specify',
        max_length=50,
        null=True,
        blank=True,
        )

    method = models.CharField(
        max_length=10,
        choices=METHOD,
        )

    organism = models.ForeignKey(Organism)

    site = models.ForeignKey(Site)

    status = models.CharField(
        max_length=10,
        choices=STATUS,
        )

    resolution_date = models.DateField()

    class Meta:
        abstract = True
