from django.contrib import admin

from ..models import ExportHistory


class ExportHistoryAdmin (admin.ModelAdmin):

    date_hierarchy = 'export_datetime'
    list_filter = ('export_datetime', )
    search_fields = ('export_pk',)

admin.site.register(ExportHistory, ExportHistoryAdmin)
