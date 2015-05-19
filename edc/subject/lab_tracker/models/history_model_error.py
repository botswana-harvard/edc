from django.db import models

from .base_history_model import BaseHistoryModel


class HistoryModelError(BaseHistoryModel):

    error_message = models.TextField(max_length=500)
    objects = models.Manager()

    class Meta:
        app_label = 'lab_tracker'
        db_table = 'bhp_lab_tracker_historymodelerror'
