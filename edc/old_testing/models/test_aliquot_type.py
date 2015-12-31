from lis.specimen.lab_aliquot_list.models import BaseAliquotType
from lis.specimen.lab_aliquot_list.managers import AliquotTypeManager


class TestAliquotType(BaseAliquotType):

    objects = AliquotTypeManager()

    class Meta:
        app_label = 'testing'
