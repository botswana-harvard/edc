from django.db import models
from django.core.exceptions import ImproperlyConfigured
from device.sync.models import BaseSyncUuidModel
from subject.appointment.choices import APPT_STATUS
from subject.appointment.constants import NEW


class SubjectConfiguration(BaseSyncUuidModel):
    """Store subject specific defaults."""

    subject_identifier = models.CharField(
        max_length=36)

    default_appt_type = models.CharField(
        max_length=10,
        default='clinic',
        choices=(('clinic', 'In clinic'), ('telephone', 'By telephone')),
        help_text=''
        )

    def __unicode__(self):
        return self.subject_identifier

    def natural_key(self):
        return (self.subject_identifier, )

    def save(self, *args, **kwargs):
        self.update_new_appointments()
        super(SubjectConfiguration, self).save(*args, **kwargs)

    def update_new_appointments(self):
        Appointment = models.get_model('appointment', 'Appointment')

        """Updates \'NEW\' appointments for this subject_identifier to reflect this appt_status."""
        if 'new' not in [x[0] for x in APPT_STATUS]:
            raise ImproperlyConfigured('SubjectConfiguration save() expects APPT_STATUS choices tuple to have a \'new\' option. Not found. Got {0}'.format(APPT_STATUS))
        for appointment in Appointment.objects.filter(registered_subject__subject_identifier=self.subject_identifier, appt_status__iexact=NEW):
            appointment.appt_type = self.default_appt_type
            appointment.raw_save()

    class Meta:
        app_label = 'subject_config'
        db_table = 'bhp_subject_config_subjectconfiguration'
