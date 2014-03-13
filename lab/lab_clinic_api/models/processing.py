from django.db import models

from edc.base.model.models import BaseUuidModel

from ..classes import SpecimenHelper

from .aliquot import Aliquot
from .processing_profile import ProcessingProfile


class Processing(BaseUuidModel):

    aliquot = models.ForeignKey(Aliquot,
        verbose_name='Source Aliquot',
        help_text='Create aliquots from this one')

    processing_profile = models.ForeignKey(ProcessingProfile,
        verbose_name='Profile')

    print_labels = models.BooleanField(
        verbose_name='Print aliquot labels now',
        default=True)

    objects = models.Manager()

    def __unicode__(self):
        return self.profile_name

    def save(self, *args, **kwargs):
        # create aliquots as per profile
        specimen_helper = SpecimenHelper()
        specimen_helper.aliquot_by_profile(self.aliquot, self.processing_profile)
        super(Processing, self).save(*args, **kwargs)

    class Meta:
        app_label = 'lab_clinic_api'
