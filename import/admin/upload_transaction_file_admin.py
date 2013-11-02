from django.contrib import admin

from ..models import UploadTransactionFile
from ..forms import UploadTransactionFileForm


class UploadTransactionFileAdmin(admin.ModelAdmin):

    form = UploadTransactionFileForm
    date_hierarchy = 'created'
    list_display = ('file_name', 'consumed', 'not_consumed', 'created', 'user_created', 'hostname_created')
    list_filter = ('created', 'hostname_created')

admin.site.register(UploadTransactionFile, UploadTransactionFileAdmin)
