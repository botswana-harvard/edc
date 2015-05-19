from django.db import models
from edc.base.model.models import BaseModel


class DerivedSubjectIdentifier(BaseModel):
    """Store subject identifiers derived from another participant, e.g. infant identifier from maternal identifier"""

    subject_identifier = models.CharField(
        max_length=25,
        unique=True)

    base_identifier = models.CharField(
        max_length=25)

    padding = models.IntegerField(null=True)

    def __unicode__(self):
        return self.subject_identifier

    class Meta:
        app_label = 'identifier'
        db_table = 'bhp_identifier_derivedsubjectidentifier'