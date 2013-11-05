from django.db import models

from edc.base.model.models import BaseModel

class UploadSkipDays(BaseModel):

    skip_date = models.DateField(unique=True)

    def save(self, *args, **kwargs):
        super(UploadSkipDays, self).save(*args, **kwargs)
        
    def __unicode__(self):
        return unicode(self.skip_date)
        
    class Meta:
        app_label = 'import'
        ordering = ('-created', )
