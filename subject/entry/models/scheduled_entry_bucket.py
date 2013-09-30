from django.db import models
from edc.subject.appointment.models import Appointment
from ..managers import ScheduledEntryBucketManager
from ..models import BaseEntryBucket
from .entry import Entry


class ScheduledEntryBucket(BaseEntryBucket):
    """Subject-specific list of required and scheduled entry as per normal visit schedule."""

    appointment = models.ForeignKey(Appointment, related_name='+')
    entry = models.ForeignKey(Entry)
    objects = ScheduledEntryBucketManager()

    def save(self, *args, **kwargs):
        # update with verbose name for display on dashboard
        self.current_entry_title = self.entry.content_type_map.content_type.model_class()._meta.verbose_name
        super(ScheduledEntryBucket, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.current_entry_title

    def is_serialized(self):
        """Don't serialize these records as they clutter up the outgoing box and can be regenerated by the consumer.

        See example in registered_subject_dashboard.py"""
        return False

    def natural_key(self):
        return self.appointment.natural_key() + self.entry.natural_key()

    class Meta:
        app_label = 'entry'
        db_table = 'bhp_entry_scheduledentrybucket'  # TODO: remove once schema is refactored
        verbose_name = "Subject Scheduled Entry Bucket"
        ordering = ['registered_subject', 'entry', 'appointment']
        unique_together = ['registered_subject', 'entry', 'appointment']
