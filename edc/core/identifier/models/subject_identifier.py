from django.db import models
from edc.device.sync.models import BaseSyncUuidModel

from .base_identifier_model import BaseIdentifierModel


class SubjectIdentifier(BaseIdentifierModel, BaseSyncUuidModel):

    objects = models.Manager()

    class Meta:
        app_label = 'identifier'
        db_table = 'bhp_identifier_subjectidentifier'
        ordering = ['-created']
