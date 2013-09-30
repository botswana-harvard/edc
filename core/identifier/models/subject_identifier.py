from django.db import models
from .base_identifier_model import BaseIdentifierModel


class SubjectIdentifier(BaseIdentifierModel):

    objects = models.Manager()

    class Meta:
        app_label = 'identifier'
        db_table = 'bhp_identifier_subjectidentifier'
        ordering = ['-created']
