from django.db import models

from edc.subject.appointment.models import Appointment
from edc.subject.entry.models import Entry

from .base_entry_meta_data import BaseEntryMetaData


class ScheduledEntryMetaData(BaseEntryMetaData):
    """Subject-specific list of required and scheduled entry as per normal visit schedule."""

    appointment = models.ForeignKey(Appointment, related_name='+')

    entry = models.ForeignKey(Entry)

    def __unicode__(self):
        return self.current_entry_title

    def is_serialized(self):
        """Don't serialize these records as they clutter up the outgoing box and can be regenerated by the consumer.

        See example in registered_subject_dashboard.py"""
        return False

    class Meta:
        app_label = 'entry_meta_data'
        verbose_name = "Scheduled Entry Metadata"
        ordering = ['registered_subject', 'entry', 'appointment']
        unique_together = ['registered_subject', 'entry', 'appointment']
