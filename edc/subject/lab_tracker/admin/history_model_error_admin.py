from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin

from ..models import HistoryModelError


class HistoryModelErrorAdmin(BaseModelAdmin):
    list_display = ('subject_identifier', 'group_name', 'test_code', 'value', 'value_datetime', 'source_model_name', 'source_app_label', 'source_identifier', 'history_datetime', 'modified')
    search_fields = ('subject_identifier', 'value', 'error_message')
    list_filter = ('group_name', 'source_model_name', 'source_app_label', 'test_code', 'modified')
    date_hierarchy = 'value_datetime'
admin.site.register(HistoryModelError, HistoryModelErrorAdmin)
