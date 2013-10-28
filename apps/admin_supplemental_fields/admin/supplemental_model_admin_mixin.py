import copy

from ..models import ExcludedHistory


class SupplementalModelAdminMixin(object):
    """Mixin class for ModelAdmin that has supplemental fields.

    Put on LEFT of declaration"""
    def __init__(self, *args):
        self._original_model_admin_fields = None
        self._group = None
        self._grouping_field = None
        super(SupplementalModelAdminMixin, self).__init__(*args)

    def save_model(self, request, obj, form, change):
        super(SupplementalModelAdminMixin, self).save_model(request, obj, form, change)
        self.update_exclude_history(obj)
        self.form._meta.exclude = None
        self._exclude_fields = None

    def contribute_to_extra_context(self, extra_context, object_id=None):
        super(SupplementalModelAdminMixin, self).contribute_to_extra_context(extra_context)
        #TODO: when is this ever False
        if self.has_excluded_supplemental_fields(object_id):
            extra_context['has_excluded_supplemental_fields'] = True
        return extra_context

    def has_excluded_supplemental_fields(self, object_id):
        if object_id:
            return ExcludedHistory.objects.filter(model_pk=object_id).exists()
        return False

    def _set_original_model_admin_fields(self):
        """Save the original fields tuple from the ModelAdmin instance.

        ... note:: the list of fields from ModelAdmin is not necessarily the same as the list of fields from the model instance."""
        self._original_model_admin_fields = copy.deepcopy(self.fields)

    def _get_original_model_admin_fields(self):
        return self._original_model_admin_fields

    def get_form_prep(self, request, obj=None, **kwargs):
        super(SupplementalModelAdminMixin, self).get_form_prep(request, obj, **kwargs)
        self.get_form_before_form_factory(request, obj, **kwargs)

    def get_form_post(self, request, obj=None, **kwargs):
        super(SupplementalModelAdminMixin, self).get_form_post(request, obj, **kwargs)
#         self.fields = self._get_original_model_admin_fields()

    def get_form_before_form_factory(self, request, obj=None, **kwargs):
        """Checks if the ModelAdmin has supplemental fields and adds or updates the decision to form._meta.exclude.

        Note that get_exclude_fields may return nothing."""
        if not request.method == 'POST':
            # set for._meta.exclude so the info is saved on ModelAdmin.save()'s call to update_excluded_model().
            # We must use the same excluded fields on Add and Change
            if not self._get_original_model_admin_fields():
                self._set_original_model_admin_fields()
            self.set_exclude_fields(obj)
            if self.form._meta.exclude:
                # TODO: i thought we were not allowing form._meta.exclude to be populated?
                self.form._meta.exclude = tuple(set(list(self.form._meta.exclude) + list(self.get_exclude_fields(obj))))
            else:
                self.form._meta.exclude = self.get_exclude_fields(obj)

    def set_exclude_fields(self, obj):
        """Sets the ModelAdmin fields attribute to reflect the choice of excluding or not excluding the supplemental fields."""
        self._exclude_fields = None
        # we are using form._meta.exclude, so make sure it was not set in the form.Meta class definition
        if 'exclude' in dir(self.form.Meta):
            raise AttributeError('The form.Meta attribute exclude cannot be used with \'supplemental_fields\'. See {0}.'.format(self.form))
        # always set to None first, note that form._meta.exclude seems to override ModelAdmin.exclude
        self.form._meta.exclude = None
        # note that self.fields, ModelAdmin fields, is updated here.
        # this is where the choice is made to exclude the supplemental fields from the ModelAdmin.fields
        # TODO: we are not using ModelAdmin.exclude but directly manipulating ModelAdmin.fields. Which is better?
        if not self.fields:
            raise AttributeError('The ModelAdmin.fields attribute must be explicitly set if class is used with \'supplemental_fields\'. See {0}.'.format(self.__class__))
        self.fields, self._exclude_fields = self.supplemental_fields.choose_fields(self._get_original_model_admin_fields(), self.model, obj)

    def get_exclude_fields(self, obj=None):
        return self._exclude_fields

    def update_exclude_history(self, obj):
        """Updates the admin_supplemental_fields Excluded history model to remember which fields were excluded on Add.

        Also, resets form._meta.exclude.

        .. seealso:: post delete signal."""
        if self.form._meta.exclude:
            # record which instances were selected for excluded fields, (see also the post_delete signal).
            if ExcludedHistory.objects.filter(app_label=obj._meta.app_label, object_name=obj._meta.object_name, model_pk=obj.pk):
                excluded_history = ExcludedHistory.objects.get(app_label=obj._meta.app_label, object_name=obj._meta.object_name, model_pk=obj.pk)
                excluded_history.excluded_fields = self.get_exclude_fields(obj)
                excluded_history.save()
            else:
                ExcludedHistory.objects.create(
                    app_label=obj._meta.app_label,
                    object_name=obj._meta.object_name,
                    model_pk=obj.pk,
                    excluded_fields=self.get_exclude_fields(obj),
                    group=self._get_group(),
                    grouping_field=self._get_grouping_field())
        # clear in case the form instance, or this instancem, is used again

    def _set_group(self, value):
        self._group = value

    def _get_group(self):
        return self._group

    def _set_grouping_field(self, value):
        self._grouping_field = value

    def _get_grouping_field(self):
        return self._grouping_field
