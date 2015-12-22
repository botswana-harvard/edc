from django.db.models import get_model
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from edc_appointment.models import Appointment
from .time_point_status import TimePointStatus


@receiver(post_save, weak=False, dispatch_uid="appointment_post_save")
def appointment_post_save(sender, instance, raw, created, using, **kwargs):
    """Creates the TimePointStatus instance if it does not already exist."""
    if not raw:
        if isinstance(instance, Appointment):
            TimePointStatus = get_model('data_manager', 'TimePointStatus')
            try:
                TimePointStatus.objects.get(appointment=instance)
            except TimePointStatus.DoesNotExist:
                TimePointStatus.objects.create(appointment=instance)


@receiver(pre_delete, weak=False, dispatch_uid="appointment_pre_delete")
def appointment_pre_delete(sender, instance, using, **kwargs):
    """Deletes the TimePointStatus instance if it exists."""
    if isinstance(instance, Appointment):
        try:
            TimePointStatus.objects.get(appointment=instance).delete()
        except TimePointStatus.DoesNotExist:
            pass
