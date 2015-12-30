from django.db import models
from django.core.exceptions import ImproperlyConfigured

from edc_appointment.choices import APPT_STATUS, APPT_TYPE
from edc_constants.constants import NEW_APPT, UNKEYED
from edc_base.model.models import BaseUuidModel
from edc_sync.models import SyncModelMixin


class SubjectConfiguration(SyncModelMixin, BaseUuidModel):
    """Store subject specific defaults."""

    subject_identifier = models.CharField(
        max_length=36)

    default_appt_type = models.CharField(
        max_length=10,
        default='clinic',
        choices=APPT_TYPE,
        help_text='')

    def __unicode__(self):
        return self.subject_identifier

    def natural_key(self):
        return (self.subject_identifier, )

    def save(self, *args, **kwargs):
        self.update_new_appointments()
        super(SubjectConfiguration, self).save(*args, **kwargs)

    def update_new_appointments(self):
        """Updates \'NEW\' appointments for this subject_identifier to reflect this appt_status."""
        Appointment = models.get_model('edc_appointment', 'Appointment')
        if NEW_APPT not in [x[0] for x in APPT_STATUS]:
            raise ImproperlyConfigured(
                'SubjectConfiguration save() expects APPT_STATUS choices tuple '
                'to have a \'{0}\' option. Not found. Got {1}'.format(NEW_APPT, APPT_STATUS))
        for appointment in Appointment.objects.filter(
                registered_subject__subject_identifier=self.subject_identifier, appt_status__iexact=UNKEYED):
            appointment.appt_type = self.default_appt_type
            appointment.raw_save()

    class Meta:
        app_label = 'subject_config'
        db_table = 'bhp_subject_config_subjectconfiguration'
