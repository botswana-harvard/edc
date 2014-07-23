from django.contrib import admin
from base.modeladmin.admin import BaseModelAdmin
from base.modeladmin.admin import BaseTabularInline
from ..models import Holiday


class HolidayAdmin(BaseModelAdmin):
    pass
admin.site.register(Holiday, HolidayAdmin)


class HolidayInlineAdmin(BaseTabularInline):
    model = Holiday
    extra = 0
