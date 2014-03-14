from django.db import models

from edc.audit.audit_trail import AuditTrail
from edc.lab.lab_requisition.models import BaseRequisition
from edc.entry_meta_data.managers import RequisitionMetaDataManager

from ..models import TestVisit


class TestRequisition(BaseRequisition):

    test_visit = models.ForeignKey(TestVisit)

    history = AuditTrail()

    entry_meta_data_manager = RequisitionMetaDataManager(TestVisit)

    def get_visit(self):
        return self.test_visit

    class Meta:
        app_label = 'testing'
