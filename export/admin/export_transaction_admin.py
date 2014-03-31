from django.contrib import admin

from ..models import ExportTransaction


class ExportTransactionAdmin (admin.ModelAdmin):

    date_hierarchy = 'created'
    list_display = ('timestamp', 'render', 'status', 'app_label', 'object_name', 'change_type', 'created',)
    list_filter = ('status', 'app_label', 'object_name', 'change_type', 'created')
    search_fields = ('tx_pk',)

admin.site.register(ExportTransaction, ExportTransactionAdmin)
