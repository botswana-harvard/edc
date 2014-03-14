from django.contrib import admin

from edc.base.admin.admin import BaseModelAdmin

from ..actions import print_aliquot_label
from ..models import Aliquot


class AliquotAdmin(BaseModelAdmin):
    date_hierarchy = 'created'

    actions = [print_aliquot_label]

    list_display = ("aliquot_identifier", 'process', 'subject_identifier', 'drawn', "aliquot_type", 'aliquot_condition', 'created', 'user_created', 'hostname_created')

    search_fields = ('aliquot_identifier', 'receive__receive_identifier', 'receive__registered_subject__subject_identifier')

    list_filter = ('aliquot_type', 'aliquot_condition', 'created', 'user_created', 'hostname_created')

    list_per_page = 15

admin.site.register(Aliquot, AliquotAdmin)
