from django.contrib import admin
from django.contrib.auth.models import Group
from edc.subject.registration.models import RegisteredSubject
from ..forms import QualityInspectionForm
from ..models import QualityInspection
from .base_admin import BaseAdmin


class QualityInspectionAdmin(BaseAdmin):

    form = QualityInspectionForm

    def __init__(self, *args, **kwargs):
        super(QualityInspectionAdmin, self).__init__(*args, **kwargs)
        self.list_display = (
            'registered_subject',
            'dashboard',
            'date_added',
            'the_visit_code',
            'status')
        self.search_fields.insert(0, 'registered_subject__pk')
        self.search_fields.insert(0, 'registered_subject__subject_identifier')

    def save_model(self, request, obj, form, change):
        """auto fill authorization when blank on save models"""
        obj.authorization = request.user
        #obj.save()
        """only giving permissions to field supervisor for final close off"""
        user_groups = [group.name for group in Group.objects.filter(user__username=request.user)]
        if obj.status == 'closed' and ('field_supervisor' not in user_groups):
            obj.status = 'open'
        super(QualityInspectionAdmin, self).save_model(request, obj, form, change)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "registered_subject":
            if request.GET.get('registered_subject'):
                kwargs["queryset"] = RegisteredSubject.objects.filter(pk=request.GET.get('registered_subject'))
        return super(QualityInspectionAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(QualityInspection, QualityInspectionAdmin)
