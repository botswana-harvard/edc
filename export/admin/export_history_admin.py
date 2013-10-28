from django.contrib import admin

from ..models import ExportHistory


class ExportHistoryAdmin (admin.ModelAdmin):

    date_hierarchy = 'sent_datetime'
    list_filter = ('sent', 'received', 'exported', 'sent_datetime', 'received_datetime', 'export_datetime')
    search_fields = ('export_pk',)

admin.site.register(ExportHistory, ExportHistoryAdmin)
