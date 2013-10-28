from django.db.models.signals import post_save
from django.dispatch import receiver
from .base_subject import BaseSubject


@receiver(post_save, weak=False, dispatch_uid='base_subject_get_or_create_registered_subject_on_post_save')
def base_subject_get_or_create_registered_subject_on_post_save(sender, instance, **kwargs):
    if isinstance(instance, (BaseSubject, )) and not sender._meta.object_name.lower() == 'registeredsubject':
        registered_subject, updated = instance.post_save_get_or_create_registered_subject()
        # TODO: is this try/except required? registered_subject, if it exists on the model, should always have a value by now
#         try:
#             if not instance.registered_subject:
#                 instance.registered_subject = registered_subject
#         except:
#             pass
        if updated:
            post_save.disconnect(base_subject_get_or_create_registered_subject_on_post_save, sender=sender)
            instance.save()
            post_save.connect(base_subject_get_or_create_registered_subject_on_post_save, sender=sender)
