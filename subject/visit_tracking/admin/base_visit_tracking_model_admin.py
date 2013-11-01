from collections import OrderedDict

from django.db.models import ForeignKey
from django.core.exceptions import ImproperlyConfigured

from edc.base.admin.admin import BaseModelAdmin
from edc.export.actions import export_as_csv_action
from edc.subject.consent.models import BaseConsentedUuidModel

from ..classes import VisitModelHelper


class BaseVisitTrackingModelAdmin(BaseModelAdmin):

    """ModelAdmin subclass for models with a ForeignKey to your visit model(s)"""

    visit_model = None
    date_hierarchy = 'report_datetime'

    def __init__(self, *args, **kwargs):
        self._visit_model_attr = None
        self._visit_model_pk = None
        super(BaseVisitTrackingModelAdmin, self).__init__(*args, **kwargs)
        self.set_visit_model()
        self.set_visit_model_fk_name()
        self.extend_list_display()
        self.extend_list_filter()
        self.extend_search_fields()

    def set_visit_model(self):
        """Checks that visit model attribute is set"""
        if not self.visit_model:
            raise ImproperlyConfigured("Class attribute \'visit model\' on BaseVisitModelAdmin for model {0} may not be None. Please correct.".format(self.model))

    def set_visit_model_fk_name(self):
        """Determine name of field that points to the visit model on this model"""
        self.visit_model_foreign_key = [fk for fk in [f for f in self.model._meta.fields if isinstance(f, ForeignKey)] if fk.rel.to._meta.module_name == self.visit_model._meta.module_name]
        if not self.visit_model_foreign_key:
            raise ValueError("The model for {0} requires a foreign key to visit model {1}. None found. Either correct the model or change the ModelAdmin class.".format(self, self.visit_model))
        else:
            self.visit_model_foreign_key = self.visit_model_foreign_key[0].name

    def extend_search_fields(self):
        if isinstance(self.search_fields, list):
            for item in ['id', self.visit_model_foreign_key + '__appointment__registered_subject__subject_identifier', self.visit_model_foreign_key + '__pk']:
                if item not in self.search_fields:
                    self.search_fields.append(item)

    def extend_list_display(self):
        """Extends list display with additional values if passed as a list."""
        if isinstance(self.list_display, list):
            for item in [self.visit_model_foreign_key, 'created', 'modified', 'user_created', 'user_modified', ]:
                if item not in self.list_display:
                    self.list_display.append(item)
            self.list_display = tuple(self.list_display)

    def extend_list_filter(self):
        """Extends list filter with additional values if passed as a list."""
        if isinstance(self.list_filter, list):
            extended_list_filter = [
                self.visit_model_foreign_key + '__report_datetime',
                self.visit_model_foreign_key + '__reason',
                self.visit_model_foreign_key + '__appointment__appt_status',
                self.visit_model_foreign_key + '__appointment__visit_definition__code',
                self.visit_model_foreign_key + '__appointment__registered_subject__study_site__site_code',
                'created',
                'modified',
                'user_created',
                'user_modified',
                'hostname_created']
            for item in extended_list_filter:
                if item not in self.list_filter:
                    self.list_filter.append(item)
            self.list_filter = tuple(self.list_filter)

    def get_actions(self, request):
        actions = super(BaseVisitTrackingModelAdmin, self).get_actions(request)
        if issubclass(self.model, BaseConsentedUuidModel):
            actions['export_as_csv_action'] = (  # This is a django SortedDict (function, name, short_description)
                export_as_csv_action(
                    exclude=['id', self.visit_model_foreign_key],
                    extra_fields=OrderedDict(
                        {'subject_identifier': self.visit_model_foreign_key + '__appointment__registered_subject__subject_identifier',
                         'visit_report_datetime': '%s__report_datetime' % self.visit_model_foreign_key,
                         'gender': self.visit_model_foreign_key + '__appointment__registered_subject__gender',
                         'dob': self.visit_model_foreign_key + '__appointment__registered_subject__dob',
                         'visit_reason': self.visit_model_foreign_key + '__reason',
                         'visit_status': self.visit_model_foreign_key + '__appointment__appt_status',
                         'visit': self.visit_model_foreign_key + '__appointment__visit_definition__code',
                         'visit_instance': self.visit_model_foreign_key + '__appointment__visit_instance'}),
                    ),
                    'export_as_csv_action',
                    "Export to CSV with visit and demographics")
        return actions

    def set_visit_model_attr(self, value):
        self._visit_model_attr = value

    def get_visit_model_attr(self):
        return self._visit_model_attr

    def set_visit_model_pk(self, value):
        self._visit_model_pk = value

    def get_visit_model_pk(self):
        return self._visit_model_pk

    def add_view(self, request, form_url='', extra_context=None):
        """Sets the values for the visit model object name and the visit model pk.

        To be used by supplemental fields, etc."""
        self.set_visit_model_attr(request.GET.get('visit_attr'))
        self.set_visit_model_pk(request.GET.get(self.get_visit_model_attr()))
        return super(BaseVisitTrackingModelAdmin, self).add_view(request, form_url=form_url, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        """Sets the values for the visit model object name and the visit model pk.

        To be used by supplemental fields, etc."""
        self.set_visit_model_attr(request.GET.get('visit_attr'))
        self.set_visit_model_pk(request.GET.get(self.get_visit_model_attr()))
        return super(BaseVisitTrackingModelAdmin, self).change_view(request, object_id, form_url=form_url, extra_context=extra_context)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        visit_model_helper = VisitModelHelper()
        if db_field.name == visit_model_helper.get_visit_field(model=self.model, visit_model=self.visit_model):
            #if not request.GET.get('subject_identifier', None):
            #    raise TypeError('Subject identifier cannot be none when accessing {0}.'.format(db_field.name))
            kwargs["queryset"] = visit_model_helper.set_visit_queryset(
                visit_model=self.visit_model,
                pk=request.GET.get(db_field.name, None),
                subject_identifier=request.GET.get('subject_identifier', 0),
                visit_code=request.GET.get('visit_code', 0),
                visit_instance=request.GET.get('visit_instance', 0))
        return super(BaseVisitTrackingModelAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
