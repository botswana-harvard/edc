from django.db import models
from edc.lab.lab_base_model.models import BaseLabModel
#from edc.lab.lab_clinic_api.managers import PanelGroupManager


class PanelGroup (BaseLabModel):

    name = models.CharField(
        verbose_name="Panel Group Name",
        max_length=25,
        unique=True,
        )

    #objects = PanelGroupManager()

    def __unicode__(self):
        return self.name

    def natural_key(self):
        return (self.name, )

    class Meta:
        app_label = 'lab_panel'
        db_table = 'bhp_lab_core_panelgroup'
