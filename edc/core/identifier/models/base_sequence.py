from django.db import models


class BaseSequence(models.Model):

    device_id = models.IntegerField(default=99)
    objects = models.Manager()

    def __unicode(self):
        return self.pk

    class Meta:
        abstract = True
