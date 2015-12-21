from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, weak=False, dispatch_uid="prepare_appointments_on_post_save")
def prepare_appointments_on_post_save(sender, instance, raw, created, using, **kwargs):
    """"""
    if not raw:
        try:
            instance.prepare_appointments(using)
        except AttributeError as e:
            if 'prepare_appointments' not in str(e):
                raise
