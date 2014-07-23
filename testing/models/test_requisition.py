from django.db import models
from audit.audit_trail import AuditTrail
from lab.lab_requisition.models import BaseRequisition
from entry_meta_data.managers import RequisitionMetaDataManager

from .test_visit import TestVisit
from .test_panel import TestPanel
from .test_aliquot_type import TestAliquotType


class TestRequisition(BaseRequisition):

    test_visit = models.ForeignKey(TestVisit)

    panel = models.ForeignKey(TestPanel)

    aliquot_type = models.ForeignKey(TestAliquotType)

    history = AuditTrail()

    entry_meta_data_manager = RequisitionMetaDataManager(TestVisit)

    def get_visit(self):
        return self.test_visit

    class Meta:
        app_label = 'testing'
