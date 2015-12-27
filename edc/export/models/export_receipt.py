# from django.core.urlresolvers import reverse
from django.db import models
from django_extensions.db.fields import UUIDField

from edc_base.model.models import BaseUuidModel
from edc_sync.models import SyncModelMixin


class ExportReceipt(SyncModelMixin, BaseUuidModel):

    export_uuid = UUIDField(
        editable=False,
        help_text="system field for export tracking.")

    app_label = models.CharField(
        max_length=64,
        )

    object_name = models.CharField(
        max_length=64,
        )

    tx_pk = models.CharField(
        max_length=36,
        )

    timestamp = models.CharField(
        max_length=50,
        null=True,
        )

    received_datetime = models.DateTimeField(
        null=True,
        help_text='date ACK received'
        )

    def __unicode__(self):
        return '{} {}'.format(self.object_name, self.export_uuid)

    def dashboard(self):
        # TODO: get this dashboard url
        return 'dashboard?'

    class Meta:
        app_label = 'export'
        ordering = ('-timestamp', )
