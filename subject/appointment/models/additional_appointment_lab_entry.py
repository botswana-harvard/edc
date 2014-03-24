from django.db import models
from edc.device.sync.models import BaseSyncUuidModel
from .appointment import Appointment


class AdditionalAppointmentLabEntry(BaseSyncUuidModel):

    '''This model is for the additional prn labs that are added on the subject dashboards'''

    appointment = models.ForeignKey(Appointment)

    lab_entry_id = models.CharField(max_length=35)

    panel_edc_name = models.CharField(max_length=50)

    class Meta:
        app_label = 'appointment'
        db_table = 'bhp_appointment_additionalappointmentlabentry'
        verbose_name = 'Additional Appointment Lab Entry'
        verbose_name_plural = 'Additional Appointment Lab Entry'
