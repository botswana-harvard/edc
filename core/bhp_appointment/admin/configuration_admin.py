from django.contrib import admin
from edc.core.bhp_base_admin.admin import BaseModelAdmin
from ..models import Configuration
from holiday_admin import HolidayInlineAdmin


class ConfigurationAdmin(BaseModelAdmin):
    inlines = [HolidayInlineAdmin, ]
admin.site.register(Configuration, ConfigurationAdmin)
