from django.db import models

# from django_extensions.db.fields import UUIDField

from edc.device.sync.models import BaseSyncUuidModel


class ExportHistory(BaseSyncUuidModel):

    app_label = models.CharField(max_length=50)

    object_name = models.CharField(max_length=50)

    instance_pk = models.CharField(max_length=32)

    change_type = models.CharField(
        max_length=1,
        choices=(('I', 'Insert'), ('U', 'Update'), ('D', 'Delete'), ),
        help_text=''
        )

    export_uuid = models.CharField(max_length=32)  # TODO: should this be a UUID field?

    sent = models.BooleanField(default=False)

    sent_datetime = models.DateTimeField()

    received = models.BooleanField(default=False)

    received_datetime = models.DateTimeField()

    exported = models.BooleanField(default=False)

    export_datetime = models.DateTimeField()

    def save(self, *args, **kwargs):
        if self.sent and self.received:
            self.exported = True
        super(ExportHistory, self).save(*args, **kwargs)

    def model_class(self):
        return models.get_model(self.app_label, self.object_name)

    def model_instance(self):
        obj = None
        if self.model_class().objects.filter(pk=self.instance_pk):
            obj = self.model_class().objects.get(pk=self.instance_pk)
        return obj

    class Meta:
        app_label = 'export'
