from ..managers import AliquotConditionManager
from edc.core.bhp_base_model.models import BaseListModel


class AliquotCondition(BaseListModel):

    objects = AliquotConditionManager()

    def __unicode__(self):
        return "%s: %s" % (self.short_name.upper(), self.name)

    class Meta:
        app_label = 'lab_clinic_api'
