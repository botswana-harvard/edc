from django.contrib import admin

from edc.base.modeladmin.admin import BaseModelAdmin

from ..models import DefaultValueLog


class DefaultValueLogAdmin(BaseModelAdmin):
    list_display = ('subject_identifier', 'group_name', 'value', 'value_datetime', 'modified')
    search_fields = ('subject_identifier', 'error_message')
    list_filter = ('group_name', 'subject_type', 'modified')
    date_hierarchy = 'value_datetime'
admin.site.register(DefaultValueLog, DefaultValueLogAdmin)
