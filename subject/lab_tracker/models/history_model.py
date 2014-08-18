from django.db import models

from .base_history_model import BaseHistoryModel


class HistoryModel(BaseHistoryModel):

    objects = models.Manager()

    class Meta:
        app_label = 'lab_tracker'
        db_table = 'bhp_lab_tracker_historymodel'
        unique_together = (('source_model_name',
                            'source_app_label',
                            'source_identifier',
                            'test_code',
                            'group_name',
                            'subject_identifier',
                            'subject_type',
                            'value_datetime'), )
