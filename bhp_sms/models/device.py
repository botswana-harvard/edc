from django.db import models
from ...bhp_base_model.models import BaseUuidModel


class Device(BaseUuidModel):
    name = models.CharField(max_length=40)
    phone = models.CharField(max_length=20)
    is_authorized = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.phone)

    class Meta:
        app_label = 'bhp_sms'
        db_table = u'device'
