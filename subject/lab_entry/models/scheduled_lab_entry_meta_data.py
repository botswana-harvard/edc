from django.db import models
from django.core.urlresolvers import reverse
from edc.subject.appointment.models import Appointment
from edc.subject.entry.models import BaseEntryMetaData
from ..managers import ScheduledLabEntryBucketManager
from .lab_entry import LabEntry


class ScheduledLabEntryMetaData(BaseEntryMetaData):

    """Subject-specific list of required and scheduled lab as per normal visit schedule."""

    appointment = models.ForeignKey(Appointment, related_name='+')

    lab_entry = models.ForeignKey(LabEntry)

    objects = ScheduledLabEntryBucketManager()

    def natural_key(self):
        return self.lab_entry.natural_key() + self.appointment.natural_key()

    def deserialize_on_duplicate(self):
        return False

    def get_absolute_url(self):
        return reverse('admin:bhp_lab_entry_scheduledlabentrybucket_change', args=(self.id,))

    def __unicode__(self):
        return '%s: %s' % (self.registered_subject.subject_identifier, self.lab_entry.panel.name)

    class Meta:
        app_label = 'lab_entry'
        db_table = 'bhp_lab_entry_scheduledlabentrybucket'
        verbose_name = "Scheduled Lab Meta Data"
        ordering = ['registered_subject', 'lab_entry__panel__name', 'appointment', ]
        unique_together = ['registered_subject', 'lab_entry', 'appointment', ]
