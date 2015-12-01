from django.db import models

from edc_base.model.fields import OtherCharField

from .base_base_death import BaseBaseDeath
from .death_list import DeathMedicalResponsibility


class BaseDeath(BaseBaseDeath):

    death_medical_responsibility = models.ForeignKey(DeathMedicalResponsibility,
        verbose_name="Who was responsible for primary medical care of the participant during the month prior to death?",
        help_text="")

    class Meta:
        abstract = True
