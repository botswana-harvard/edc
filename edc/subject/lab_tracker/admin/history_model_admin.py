from django.contrib import admin

from edc.base.modeladmin.admin import BaseModelAdmin

from ..actions import update_lab_tracker
from ..models import HistoryModel


class HistoryModelAdmin(BaseModelAdmin):
    list_display = ('subject_identifier', 'dashboard', 'subject_type', 'group_name', 'test_code', 'value', 'value_datetime', 'source_model_name', 'source_app_label', 'source_identifier', 'history_datetime', 'modified')
    search_fields = ('subject_identifier', 'value', 'source_identifier')
    list_filter = ('subject_type', 'group_name', 'source_model_name', 'source_app_label', 'test_code', 'modified')
    actions = [update_lab_tracker, ]
    date_hierarchy = 'value_datetime'
admin.site.register(HistoryModel, HistoryModelAdmin)
