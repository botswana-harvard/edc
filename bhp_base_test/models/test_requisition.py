from django.db import models
from edc_lab.lab_requisition.models import BaseRequisition
from edc_core.audit_trail.audit import AuditTrail
from ..models import TestVisit


class TestRequisition(BaseRequisition):

    test_visit = models.ForeignKey(TestVisit)

    history = AuditTrail()

    class Meta:
        app_label = 'bhp_base_test'
