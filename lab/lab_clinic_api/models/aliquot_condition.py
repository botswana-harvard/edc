from edc.base.model.models import BaseListModel
from ..managers import AliquotConditionManager


class AliquotCondition(BaseListModel):

    objects = AliquotConditionManager()

    def __unicode__(self):
        return "%s: %s" % (self.short_name.upper(), self.name)

    class Meta:
        app_label = 'lab_clinic_api'
