from django.db import models

from edc_base.model.models import BaseUuidModel
from edc_sync.models import SyncModelMixin

from .base_identifier_model import BaseIdentifierModel


class SubjectIdentifier(BaseIdentifierModel, SyncModelMixin, BaseUuidModel):

    objects = models.Manager()

    class Meta:
        app_label = 'identifier'
        db_table = 'bhp_identifier_subjectidentifier'
        ordering = ['-created']
