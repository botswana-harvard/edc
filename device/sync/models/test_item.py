from django.db import models

from edc.audit.audit_trail import AuditTrail

from .base_sync_uuid_model import BaseSyncUuidModel


class TestItem(BaseSyncUuidModel):

    test_item_identifier = models.CharField(max_length=35, unique=True)

    comment = models.CharField(max_length=50, null=True)

    history = AuditTrail()

    class Meta:
        app_label = 'sync'
        db_table = 'bhp_sync_testitem'
