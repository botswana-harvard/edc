from django.db import models

from edc.subject.appointment.models import Appointment
from edc.subject.entry.models import LabEntry

from ..managers import NaturalKeyRequisitionMetaDataManager
from .base_entry_meta_data import BaseEntryMetaData


class RequisitionMetaData(BaseEntryMetaData):

    """Subject-specific list of required and scheduled lab as per normal visit schedule."""

    appointment = models.ForeignKey(Appointment, related_name='+')

    lab_entry = models.ForeignKey(LabEntry)

    objects = NaturalKeyRequisitionMetaDataManager()

    def __unicode__(self):
        return '%s: %s' % (self.registered_subject.subject_identifier, self.lab_entry.requisition_panel.name)

#     def is_serialized(self):
#         """Don't serialize these records as they clutter up the outgoing box and can be regenerated by the consumer.
# 
#         See example in registered_subject_dashboard.py"""
#         return False
    def natural_key(self):
        return self.appointment.natural_key() + self.lab_entry.natural_key()

    def deserialize_get_missing_fk(self, attrname):
        retval = None
        if attrname == 'registered_subject':
            return self.registered_subject
        if attrname == 'appointment':
            return self.appointment
        return retval

    class Meta:
        app_label = 'entry_meta_data'
        verbose_name = "Requisition Meta Data"
        ordering = ['registered_subject', 'lab_entry__requisition_panel__name', 'appointment', ]
        unique_together = ['registered_subject', 'lab_entry', 'appointment', ]
