from edc.lab.lab_profile.classes import LabProfile

from edc.testing.models import TestAliquot, TestAliquotType, TestRequisition, TestPanel, TestProfile, TestProfileItem
from edc.testing.models import TestReceive


class TestLabProfile(LabProfile):
    profile_group_name = 'test'
    aliquot_model = TestAliquot
    aliquot_type_model = TestAliquotType
    panel_model = TestPanel
    receive_model = TestReceive
    profile_model = TestProfile
    profile_item_model = TestProfileItem
    requisition_model = TestRequisition
    name = TestRequisition._meta.object_name
