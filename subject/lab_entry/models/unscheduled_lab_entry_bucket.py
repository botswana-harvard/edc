from django.db import models
from django.core.urlresolvers import reverse
from edc.subject.appointment.models import Appointment
from edc.subject.entry.models import BaseEntryMetaData
from ..managers import ScheduledLabEntryBucketManager
from .lab_entry_unscheduled import LabEntryUnscheduled


class UnscheduledLabEntryBucket(BaseEntryMetaData):

    """Subject-specific list of unscheduled labs."""

    appointment = models.ForeignKey(Appointment, related_name='+')

    lab_entry_unscheduled = models.ForeignKey(LabEntryUnscheduled)

    objects = ScheduledLabEntryBucketManager()

    def deserialize_on_duplicate(self):
        return False

    def get_absolute_url(self):
        return reverse('admin:bhp_lab_entry_unscheduledlabentrybucket_change', args=(self.id,))

    def __unicode__(self):
        return '%s: %s' % (self.registered_subject.subject_identifier, self.lab_entry_unscheduled.panel.name)

    class Meta:
        app_label = 'lab_entry'
        db_table = 'bhp_lab_entry_unscheduledlabentrybucket'
        verbose_name = "Unscheduled Lab Bucket"
        ordering = ['registered_subject', 'lab_entry_unscheduled__panel__name', 'appointment', ]
        unique_together = ['registered_subject', 'lab_entry_unscheduled', 'appointment', ]
