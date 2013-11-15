from django.db import models
from edc.base.model.models import BaseModel

class BaseReport(BaseModel):
    
    report_name = models.CharField(
        verbose_name=("report name"),
        max_length=25,
        unique=True,
        )
    
    objects = models.Manager()
    
    def __unicode__(self):
        return '{0}'.format(
            self.report_name)
    
    class Meta:
        app_label = 'bhp_birt_reports'