from datetime import datetime

from django.db import models
from django_extensions.db.fields import UUIDField


class ExportTrackingFieldsMixin(models.Model):

    """Adds these fields to the Concrete model."""

    exported = models.BooleanField(default=False, editable=False, help_text="considered 'exported' if both sent and received.")

    exported_datetime = models.DateTimeField(editable=False, null=True)

    export_change_type = models.CharField(
        max_length=1,
        choices=(('I', "Insert"), ('U', "Update"), ('D', "Delete"),),
        default='I')

    export_uuid = UUIDField()

    def update_export_mixin_fields(self):
        self.exported = True
        self.exported_datetime = datetime.now()
        self.save()

    class Meta:
        abstract = True
