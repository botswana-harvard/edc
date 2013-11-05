from django.contrib import admin

from ..models import UploadSkipDays


class UploadSkipDaysAdmin(admin.ModelAdmin):

    date_hierarchy = 'created'
    list_display = ('skip_date', 'created', 'user_created', 'hostname_created')
    list_filter = ('created', 'hostname_created')

admin.site.register(UploadSkipDays, UploadSkipDaysAdmin)
