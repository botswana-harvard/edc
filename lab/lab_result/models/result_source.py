from django.db import models
from edc.base.model.models import BaseListModel


class ResultSource(BaseListModel):

    objects = models.Manager()

    class Meta:
        app_label = 'lab_result'
        db_table = 'bhp_lab_core_resultsource'
