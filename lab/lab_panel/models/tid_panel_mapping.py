from django.db import models
from edc.core.bhp_base_model.models import BaseModel
from edc.lab.lab_panel.models import Panel


class TidPanelMapping(BaseModel):

    tid = models.CharField(
        verbose_name='dmis TID',
        max_length=3,
        )

    panel = models.ForeignKey(Panel)

    def __unicode__(self):
        return '%s->%s' % (self.tid, self.panel)

    class Meta:
        app_label = 'lab_panel'
        db_table = 'bhp_lab_core_tidpanelmapping'
