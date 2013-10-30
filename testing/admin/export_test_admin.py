from django.contrib import admin

from ..models import ExportTest


class ExportTestAdmin (admin.ModelAdmin):

    date_hierarchy = 'created'

admin.site.register(ExportTest, ExportTestAdmin)
