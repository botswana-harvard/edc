from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin

from ..models import Netbook, NetbookUser


class NetbookAdmin (BaseModelAdmin):
    list_display = (
        'name',
        'is_active',
        'db_name',
        'make',
        'model',
        'ip_address',
        'is_alive',
        'last_seen',
        'serial_number'
        )
    list_per_page = 25
    list_filter = ('is_active', 'is_alive')

admin.site.register(Netbook, NetbookAdmin)


class NetbookUserAdmin (BaseModelAdmin):
    list_display = ('netbook', 'user', 'start_date', 'end_date')
    list_per_page = 25

admin.site.register(NetbookUser, NetbookUserAdmin)
