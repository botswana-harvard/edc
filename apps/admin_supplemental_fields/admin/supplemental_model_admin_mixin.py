import copy

from django.core.exceptions import ImproperlyConfigured

from ..models import ExcludedHistory


class SupplementalModelAdminMixin(object):
    """Mixin class for ModelAdmin that has supplemental fields.

    Put on LEFT of declaration"""
    def __init__(self, *args):
        super(SupplementalModelAdminMixin, self).__init__(*args)
        self._supplemental_exclude_fields = None
        if 'Meta' not in dir(self.form):
            raise ImproperlyConfigured('ModelAdmin classes that use SupplementalFields must declare a form. See {0}'.format(self.__class__))
        if 'exclude' in dir(self.form.Meta):
            raise AttributeError('The form.Meta attribute exclude cannot be used with \'supplemental_fields\'. See {0}.'.format(self.form))
        if not self.fields:
            raise AttributeError('The ModelAdmin.fields attribute must be explicitly set if class is used with \'supplemental_fields\'. See {0}.'.format(self.__class__))
        self.supplemental_fields.original_model_admin_fields = copy.deepcopy(self.fields)  # Save the original fields tuple from the ModelAdmin instance.
        self.supplemental_fields.model = self.model

    @property
    def supplemental_exclude_fields(self):
        """Returns the ModelAdmin fields attribute to reflect the choice of excluding or not excluding the supplemental fields."""
        return self._supplemental_exclude_fields

    @supplemental_exclude_fields.setter
    def supplemental_exclude_fields(self, fields):
        self.form._meta.exclude = None
        self._supplemental_exclude_fields = fields
        return self._supplemental_exclude_fields

    def save_model(self, request, obj, form, change):
        super(SupplementalModelAdminMixin, self).save_model(request, obj, form, change)
        self.supplemental_fields.create_or_update_history(obj)
        self.supplemental_exclude_fields = None

    def add_view(self, request, form_url='', extra_context=None):
        extra_context = extra_context if extra_context else {}
        extra_context.update({'uses_supplemental_fields': True})
        self.fields = self.supplemental_fields.choose_fields()
        return super(SupplementalModelAdminMixin, self).add_view(request, form_url=form_url, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context if extra_context else {}
        extra_context.update({
            'uses_supplemental_fields': True,
            'has_excluded_supplemental_fields': ExcludedHistory.objects.filter(model_pk=object_id).exists()
            })
        self.fields = self.supplemental_fields.choose_fields()
        return super(SupplementalModelAdminMixin, self).change_view(request, object_id, form_url=form_url, extra_context=extra_context)

    def get_form_prep(self, request, obj=None, **kwargs):
        super(SupplementalModelAdminMixin, self).get_form_prep(request, obj, **kwargs)
        self.get_form_before_form_factory(request, obj, **kwargs)

    def get_form_post(self, request, obj=None, **kwargs):
        super(SupplementalModelAdminMixin, self).get_form_post(request, obj, **kwargs)
        self.fields = self.original_model_admin_fields

    def get_form_before_form_factory(self, request, obj=None, **kwargs):
        """Checks if the ModelAdmin has supplemental fields and adds or updates the decision to form._meta.exclude.

        Note that get_exclude_fields may return nothing."""
        if not request.method == 'POST':
            # set for._meta.exclude so the info is saved on ModelAdmin.save()'s call to update_excluded_model().
            # We must use the same excluded fields on Add and Change
            if self.form._meta.exclude:
                # TODO: i thought we were not allowing form._meta.exclude to be populated in its initial state?
                self.form._meta.exclude = tuple(set(list(self.form._meta.exclude) + list(self.supplemental_exclude_fields)))
            else:
                self.form._meta.exclude = self.supplemental_exclude_fields
