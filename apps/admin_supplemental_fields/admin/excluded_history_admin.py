from django.contrib import admin
from base.modeladmin.admin import BaseModelAdmin
from ..models import ExcludedHistory


class ExcludedHistoryAdmin(BaseModelAdmin):
    list_display = ('id', 'group', 'app_label', 'object_name', 'created', 'modified')
    list_filter = ('app_label', 'object_name', 'group')
admin.site.register(ExcludedHistory, ExcludedHistoryAdmin)
