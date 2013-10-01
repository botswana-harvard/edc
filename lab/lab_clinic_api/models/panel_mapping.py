from django.db import models
from edc.lab.base.model.models import BaseLabUuidModel
from edc.lab.lab_panel.models import Panel


class PanelMapping(BaseLabUuidModel):

    panel_text = models.CharField(
        max_length=50,
        help_text='text name of external panel',
        )

    panel = models.ForeignKey(Panel,
        null=True,
        help_text="local panel definition"
        )

    def __unicode__(self):
        return self.panel

    class Meta:
        app_label = "lab_clinic_api"
