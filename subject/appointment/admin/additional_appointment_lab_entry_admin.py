from django.contrib import admin

from edc.base.admin.admin import BaseModelAdmin

from ..models import AdditionalAppointmentLabEntry

from ..forms import AdditionalAppointmentLabEntryForm


class AdditionalAppointmentLabEntryAdmin(BaseModelAdmin):

    """ModelAdmin class to handle additional lab entries."""

    form = AdditionalAppointmentLabEntryForm

    fields = (
        'appointment',
        'lab_entry_id',
        'panel_edc_name',)
    list_filter = (
        'created',
        'user_created',
        'hostname_created',)
admin.site.register(AdditionalAppointmentLabEntry, AdditionalAppointmentLabEntryAdmin)
