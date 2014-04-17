# from django.core.urlresolvers import reverse
from django.db import models
from django_extensions.db.fields import UUIDField

from edc.device.sync.models import BaseSyncUuidModel


class ExportReceipt(BaseSyncUuidModel):

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

    received_datetime = models.BooleanField(
        default=False,
        help_text='date ACK received'
        )

    def dashboard(self):
        # TODO: get this dashboard url
        return 'dashboard?'

#     def render(self):
#         url = reverse('view_transaction_url', kwargs={'app_label': self._meta.app_label, 'model_name': self._meta.object_name.lower(), 'pk': self.pk})
#         ret = """<a href="{url}" class="add-another" id="add_id_report" onclick="return showAddAnotherPopup(this);"> <img src="/static/admin/img/icon_addlink.gif" width="10" height="10" alt="View transaction"/></a>""".format(url=url)
#         return ret
#     render.allow_tags = True

    class Meta:
        app_label = 'export'
        ordering = ('-timestamp', )
