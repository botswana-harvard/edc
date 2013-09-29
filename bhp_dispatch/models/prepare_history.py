from datetime import datetime
from django.db import models
from ...bhp_base_model.models import BaseUuidModel
from ...bhp_sync.models import Producer


class PrepareHistory(BaseUuidModel):
    """Tracks the history of running :func:`prepare_device` for producer."""
    source = models.CharField(max_length=50)
    destination = models.CharField(max_length=50)
    producer = models.ForeignKey(Producer)
    prepare_datetime = models.DateTimeField(default=datetime.today())
    objects = models.Manager()

    def __unicode__(self):
        return "{0} @ {1}".format(self.producer.name, self.prepare_datetime)

    class Meta:
        app_label = "bhp_dispatch"
