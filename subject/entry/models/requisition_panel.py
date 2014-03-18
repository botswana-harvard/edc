from django.db import models

from edc.base.model.models import BaseUuidModel


class RequisitionPanel(BaseUuidModel):
    """Relates to 'lab_entry' to indicate the requisition panel.

    This is usually kept in line with the protocol specific panel model data."""
    name = models.CharField(max_length=25)

    aliquot_type_alpha_code = models.CharField(max_length=4)

    objects = models.Manager()

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = 'entry'
