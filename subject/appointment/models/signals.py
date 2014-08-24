from django.db import IntegrityError
from django.db.models import get_model
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


from .appointment import Appointment
from .pre_appointment_contact import PreAppointmentContact


@receiver(post_save, weak=False, dispatch_uid="pre_appointment_contact_on_post_save")
def pre_appointment_contact_on_post_save(sender, instance, **kwargs):
    """Calls post_save method which will only call save."""
    if isinstance(instance, PreAppointmentContact):
        instance.post_save()


@receiver(post_delete, weak=False, dispatch_uid="pre_appointment_contact_on_post_delete")
def pre_appointment_contact_on_post_delete(sender, instance, **kwargs):
    """Calls post_delete method."""
    if isinstance(instance, PreAppointmentContact):
        instance.post_delete()


@receiver(post_save, weak=False, dispatch_uid="appointment_post_save")
def appointment_post_save(sender, instance, **kwargs):
    """Calls post_save method which will only call save."""
    if isinstance(instance, Appointment):
        TimePointStatus = get_model('bhp_data_manager', 'TimePointStatus')
        try:
            TimePointStatus.objects.create(appointment=instance)
        except IntegrityError:
            pass
