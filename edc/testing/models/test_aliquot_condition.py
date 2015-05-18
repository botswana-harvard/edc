from lis.specimen.lab_aliquot_list.models import BaseAliquotCondition
from lis.specimen.lab_aliquot_list.managers import AliquotConditionManager


class TestAliquotCondition(BaseAliquotCondition):

    objects = AliquotConditionManager()

    class Meta:
        app_label = 'testing'
