from django.db import models

from edc.base.model.models import BaseUuidModel

from .aliquot_type import AliquotType


class ProcessingProfile(BaseUuidModel):

    profile_name = models.CharField(
        verbose_name='Profile Name',
        max_length=25,
        unique=True)

    aliquot_type = models.ForeignKey(AliquotType,
        verbose_name='Source aliquot type')

    objects = models.Manager()

    def __unicode__(self):
        return self.profile_name

    class Meta:
        app_label = 'lab_clinic_api'


class ProcessingProfileItem(BaseUuidModel):

    processing_profile = models.ForeignKey(ProcessingProfile)

    aliquot_type = models.ForeignKey(AliquotType)

    count = models.IntegerField(default=1)

    def __unicode__(self):
        return self.aliquot_type

    class Meta:
        app_label = 'lab_clinic_api'
