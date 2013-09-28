from django.contrib import admin
from ...bhp_base_admin.admin import BaseModelAdmin
from ...bhp_base_admin.admin import BaseTabularInline
from ..models import Holiday


class HolidayAdmin(BaseModelAdmin):
    pass
admin.site.register(Holiday, HolidayAdmin)


class HolidayInlineAdmin(BaseTabularInline):
    model = Holiday
    extra = 0
