from datetime import datetime

from django_extensions.db.fields import UUIDField

from django.db import models
from django.core.exceptions import ValidationError

from edc.device.sync.models import BaseSyncUuidModel


class ExportHistory(BaseSyncUuidModel):

    app_label = models.CharField(max_length=50)

    object_name = models.CharField(max_length=50)

    instance_pk = models.CharField(max_length=36)

    change_type = models.CharField(
        max_length=2,
        choices=(('I', 'Insert'), ('U', 'Update'), ('D', 'Delete'), ('NA', 'Not applicable')),
        help_text=''
        )

    export_uuid = UUIDField()

    sent = models.BooleanField(default=False)

    sent_datetime = models.DateTimeField(null=True)

    received = models.BooleanField(default=False)

    received_datetime = models.DateTimeField(null=True)

    exported = models.BooleanField(default=False, help_text="considered 'exported' if both sent and received.")

    export_datetime = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        if self.sent and self.received and not self.exported:
            self.update_target_model()
            self.exported = True
            self.export_datetime = datetime.now()
        # TODO: may also want to raise a ValidationError is received_datetime greater than sent, etc
        super(ExportHistory, self).save(*args, **kwargs)

    def model_class(self):
        return models.get_model(self.app_label, self.object_name)

    def model_instance(self):
        obj = None
        if self.model_class().objects.filter(pk=self.instance_pk):
            obj = self.model_class().objects.get(pk=self.instance_pk)
        return obj

    def update_target_model(self):
        """Updates the target model as exported triggered by an update to the instance."""
        target_model_cls = models.get_model(self.app_label, self.object_name)
        if not target_model_cls:
            raise ValidationError('Model not found using {0}.{1}'.format(self.app_label, self.object_name))
        if not target_model_cls.objects.filter(pk=self.instance_pk):
            raise ValidationError('Instance not found for {0}.{1} pk={2}'.format(self.app_label, self.object_name, self.instance_pk))
        target_model_cls.objects.filter(pk=self.instance_pk).update(exported=True, exported_datetime=datetime.today(), export_uuid=self.export_uuid)

    class Meta:
        app_label = 'export'
        ordering = ('-sent_datetime', )
