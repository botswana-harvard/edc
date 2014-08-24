from django.contrib import admin
from django.contrib.auth.models import Group

from edc.subject.appointment.models import Appointment

from ..forms import TimePointCompletionForm
from ..models import TimePointCompletion

from .base_admin import BaseAdmin


class TimePointCompletionAdmin(BaseAdmin):

    form = TimePointCompletionForm

    def __init__(self, *args, **kwargs):
        super(TimePointCompletionAdmin, self).__init__(*args, **kwargs)
        self.list_display = (
            'appointment',
            'dashboard',
            'close_datetime',
            'status',
            'subject_withdrew')
        self.search_fields.insert(0, 'appointment__registered_subject__subject_identifier')
        self.list_filter = (
            'status',
            'close_datetime'
            'appointment__registered_subject__gender',
            'appointment__visit_definition__code'
            'subject_withdrew',
        )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "appointment":
            if request.GET.get('appointment'):
                kwargs["queryset"] = Appointment.objects.filter(pk=request.GET.get('appointment'))
        return super(TimePointCompletionAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(TimePointCompletion, TimePointCompletionAdmin)
