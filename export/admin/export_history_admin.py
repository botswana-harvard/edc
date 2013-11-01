from django.contrib import admin

from ..models import ExportHistory


class ExportHistoryAdmin (admin.ModelAdmin):

    date_hierarchy = 'sent_datetime'
    list_display = ('export_uuid', 'user_created', 'app_label', 'object_name', 'sent', 'sent_datetime', 'received', 'received_datetime', 'exported', 'export_datetime')
    list_filter = ('app_label', 'object_name', 'sent', 'received', 'exported', 'sent_datetime', 'received_datetime', 'export_datetime', 'user_created')
    search_fields = ('export_uuid',)

admin.site.register(ExportHistory, ExportHistoryAdmin)
