from datetime import datetime

from django.db import models

# from edc_base.model.models import BaseUuidModel


class PendingIdentifier(models.Model):
    """Not used."""
    pending_identifier = models.CharField(max_length=50)
    app_name = models.CharField(max_length=50)
    final_identifier = models.CharField(max_length=50, null=True)
    pending_datetime = models.DateTimeField(default=datetime.today())
    final_datetime = models.DateTimeField(null=True)
    objects = models.Manager()

    def __unicode(self):
        return self.pending_identifier

    class Meta:
        app_label = 'identifier'
        db_table = 'bhp_identifier_pendingidentifier'
        ordering = ['id', ]
