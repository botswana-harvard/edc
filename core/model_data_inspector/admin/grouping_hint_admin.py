from django.contrib import admin

from base.modeladmin.admin import BaseModelAdmin

from ..models import GroupingHint


class GroupingHintAdmin(BaseModelAdmin):

    list_filter = ('app_label', 'model_name')
    list_display = ('app_label', 'model_name', 'field_name')
admin.site.register(GroupingHint, GroupingHintAdmin)
