from django.db import models

from edc_base.model.models import BaseUuidModel
from edc_sync.models import SyncModelMixin


class IdentifierTracker(SyncModelMixin, BaseUuidModel):

    """
    A lockable model to create and track unique identifiers for new records such as requsitions, receive, etc.

    See also, classes/identifier.py

    """

    identifier = models.CharField(
        max_length=25,
        db_index=True,
        )

    identifier_string = models.CharField(
        max_length=50,
        db_index=True,
        )

    root_number = models.IntegerField(db_index=True)

    counter = models.IntegerField(db_index=True)

    identifier_type = models.CharField(
        max_length=35
        )

    device_id = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        )

    objects = models.Manager()

    def is_serialized(self):
        return True

    def __unicode__(self):
        return self.identifier

    class Meta:
        app_label = 'identifier'
        db_table = 'bhp_identifier_identifiertracker'
        ordering = ['root_number', 'counter']
        unique_together = ['root_number', 'counter']
