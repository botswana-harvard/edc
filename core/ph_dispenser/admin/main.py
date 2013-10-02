from django.contrib import admin
from edc.base.admin.admin import BaseModelAdmin
from ph_dispenser.actions import print_dispensing_label
from ph_dispenser.models import Dispensing


class DispensingAdmin(BaseModelAdmin):

    list_display = ('identifier', 'subject_identifier', 'sid', 'copies', 'dispense_date', 'user_created', 'created')
    actions = [print_dispensing_label]
    list_per_page = 25
    search_fields = ('subject_identifier', 'sid', 'identifier')
    list_filter = ('dispense_date', 'user_created', 'created')

admin.site.register(Dispensing, DispensingAdmin)
