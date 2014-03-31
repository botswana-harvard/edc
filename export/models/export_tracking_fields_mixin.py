from django.db import models
from django_extensions.db.fields import UUIDField


class ExportTrackingFieldsMixin(models.Model):

    """Adds these fields to the Concrete model."""

    exported = models.BooleanField(default=False, editable=False, help_text="considered 'exported' if both sent and received.")

    exported_datetime = models.DateTimeField(editable=False, null=True)

    export_uuid = UUIDField()

    class Meta:
        abstract = True
