from django.core.urlresolvers import reverse
from django.db import models
from edc.base.model.models import BaseUuidModel

from .export_tracking_fields_mixin import ExportTrackingFieldsMixin


class ExportTransaction(BaseUuidModel, ExportTrackingFieldsMixin):

    tx = models.TextField()

    app_label = models.CharField(
        max_length=64,
        db_index=True,
        )

    object_name = models.CharField(
        max_length=64,
        db_index=True,
        )

    tx_pk = models.CharField(
        max_length=36,
        )

    timestamp = models.CharField(
        max_length=50,
        null=True,
        db_index=True,
        )

    status = models.CharField(
        max_length=15,
        default='new',
        choices=(
            ('exported', 'Exported'),
            ('closed', 'Closed'),
            ('new', 'New'),
            ('cancelled', 'Cancelled'),
            ),
        )

    is_ignored = models.BooleanField(
        default=False,
        db_index=True,
        help_text='Ignore if update'
        )

    is_error = models.BooleanField(
        default=False,
        db_index=True,
        )

    objects = models.Manager()

    def is_serialized(self):
        return False

    def dashboard(self):
        # TODO: get this dashboard url
        return 'dashboard?'

    def render(self):
        url = reverse('view_transaction_url', kwargs={'app_label': self._meta.app_label, 'model_name': self._meta.object_name.lower(), 'pk': self.pk})
        ret = """<a href="{url}" class="add-another" id="add_id_report" onclick="return showAddAnotherPopup(this);"> <img src="/static/admin/img/icon_addlink.gif" width="10" height="10" alt="View transaction"/></a>""".format(url=url)
        return ret
    render.allow_tags = True

    class Meta:
        app_label = 'export'
        ordering = ('-timestamp', )
