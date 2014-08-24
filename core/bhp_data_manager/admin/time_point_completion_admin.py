from django.contrib import admin
from django.contrib.auth.models import Group
from edc.subject.registration.models import RegisteredSubject
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
            'close_date',
            'status',
            'subject_withdrew')
        self.search_fields.insert(0, 'registered_subject__subject_identifier')
        self.list_filter = (
            'status',
            'close_date'
            'appointment__registered_subject__gender',
            'appointment__visit_definition__code'
            'subject_withdrew',
        )

    def save_model(self, request, obj, form, change):
        """auto fill authorization when blank on save models"""
        obj.authorization = request.user
        obj.save()
#         """only giving permissions to field supervisor for final close off"""
#         user_groups = [group.name for group in Group.objects.filter(user__username=request.user)]
#         if obj.status == 'closed' and ('field_supervisor' not in user_groups):
#             obj.status = 'open'
        super(TimePointCompletionAdmin, self).save_model(request, obj, form, change)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "registered_subject":
            if request.GET.get('registered_subject'):
                kwargs["queryset"] = RegisteredSubject.objects.filter(pk=request.GET.get('registered_subject'))
        if db_field.name == "appointment":
            if request.GET.get('appointment'):
                kwargs["queryset"] = Appointment.objects.filter(pk=request.GET.get('appointment'))
        return super(TimePointCompletionAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(TimePointCompletion, TimePointCompletionAdmin)