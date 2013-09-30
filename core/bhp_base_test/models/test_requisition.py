from django.db import models
from edc.lab.lab_requisition.models import BaseRequisition
from edc.audit.audit_trail import AuditTrail
from ..models import TestVisit


class TestRequisition(BaseRequisition):

    test_visit = models.ForeignKey(TestVisit)

    history = AuditTrail()

    class Meta:
        app_label = 'bhp_base_test'
