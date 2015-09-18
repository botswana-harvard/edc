from django.db import models
<<<<<<< Updated upstream
from edc.device.sync.models import BaseSyncUuidModel
=======
>>>>>>> Stashed changes

from .base_identifier_model import BaseIdentifierModel


class SubjectIdentifier(BaseIdentifierModel, BaseSyncUuidModel):

    objects = models.Manager()

    class Meta:
        app_label = 'identifier'
        db_table = 'bhp_identifier_subjectidentifier'
        ordering = ['-created']
