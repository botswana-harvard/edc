from django.contrib import admin

from ..models import UploadExportReceiptFile
from ..forms import UploadExportReceiptFileForm


class UploadExportReceiptFileAdmin(admin.ModelAdmin):

    form = UploadExportReceiptFileForm
    date_hierarchy = 'created'
    list_display = ('file_name', 'accepted', 'duplicate', 'total', 'errors', 'created', 'user_created', 'hostname_created')
    list_filter = ('created', 'hostname_created')

admin.site.register(UploadExportReceiptFile, UploadExportReceiptFileAdmin)
