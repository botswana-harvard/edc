from django.contrib import admin
from django.contrib.auth.models import Group
from edc.subject.registration.models import RegisteredSubject
from ..forms import TimePointCompletionForm
from ..models import TimePointCompletion
from .base_admin import BaseAdmin


class TimePointCompletionAdmin(BaseAdmin):

    form = TimePointCompletionForm

    def __init__(self, *args, **kwargs):
        super(TimePointCompletionAdmin, self).__init__(*args, **kwargs)
        self.list_display = (
            'registered_subject',
            'dashboard',
            'date_added',
            'the_visit_code',
            #'appointment',
            'status',
            'subject_withdrew')
        self.search_fields.insert(0, 'registered_subject__subject_identifier')
        self.list_filter = (
        'registered_subject',
        #'the_visit_code',
        'status',
        'subject_withdrew',
        'appointment__visit_definition__code'
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
        return super(TimePointCompletionAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(TimePointCompletion, TimePointCompletionAdmin)
