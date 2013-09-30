from django.contrib import admin
from edc.base.admin.admin import BaseModelAdmin
from ..models import Excluded


class ExcludedAdmin(BaseModelAdmin):
    list_display = ('id', 'app_label', 'object_name', 'created', 'modified')
    list_filter = ('app_label', 'object_name')
admin.site.register(Excluded, ExcludedAdmin)
