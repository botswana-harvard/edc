from django.contrib import admin

from edc.base.admin.admin import BaseModelAdmin

from ..models import Aliquot


class AliquotAdmin(BaseModelAdmin):
    list_display = ("aliquot_identifier", 'to_receive', 'subject_identifier', 'drawn', "aliquot_type", 'aliquot_condition', 'created', 'modified', 'import_datetime')
    search_fields = ('aliquot_identifier', 'receive__receive_identifier', 'receive__registered_subject__subject_identifier')
    list_filter = ('created', 'import_datetime', 'aliquot_type', 'aliquot_condition')
    list_per_page = 15

    def get_readonly_fields(self, request, obj):
        return [field.name for field in obj._meta.fields if field.editable]

admin.site.register(Aliquot, AliquotAdmin)
