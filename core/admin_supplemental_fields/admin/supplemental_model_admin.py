from edc.base.admin.admin import BaseModelAdmin
from ..models import Excluded


class SupplementalModelAdmin(BaseModelAdmin):
    """Base class for ModelAdmin that has supplemental fields."""

    def __init__(self, *args):
        self._exclude_fields = None
        super(SupplementalModelAdmin, self).__init__(*args)

    def save_model(self, request, obj, form, change):
        """Saves as normal but after save, updates the exclude history for supplemental fields."""
        super(SupplementalModelAdmin, self).save_model(request, obj, form, change)
        self.update_exclude_history(obj)

    def get_form_before_form_factory(self, request, obj=None, **kwargs):
        """Checks if the AmodelAdmin has supplemental fields and adds or updates the decision to form._meta.exclude.

        Note that get_exclude_fields may return nothing."""
        if not request.method == 'POST':
            # set for._meta.exclude so the info is saved on ModelAdmin.save()'s call to update_excluded_model().
            # We must use the same excluded fields on Add and Change
            if self.form._meta.exclude:
                # TODO: i thought we were not allowing form._meta.exclude to be populated?
                self.form._meta.exclude = tuple(set(list(self.form._meta.exclude) + list(self.get_exclude_fields(obj))))
            else:
                self.form._meta.exclude = self.get_exclude_fields(obj)

    def set_exclude_fields(self, obj):
        """Sets the ModelAdmin fields attribute to reflect the choice of excluding or not the supplemental fields."""
        self._exclude_fields = None
        # we are using form._meta.exclude, so make sure it was not set in the form.Meta class definition
        if 'exclude' in dir(self.form.Meta):
            raise AttributeError('The form.Meta attribute exclude cannot be used with \'supplemental_fields\'. See {0}.'.format(self.form))
        # always set to None first, note that form._meta.exclude seems to override ModelAdmin.exclude
        self.form._meta.exclude = None
        # note that self.fields, ModelAdmin fields, is updated here.
        # this is where the choice is made to exclude the supplemental fields from the ModelAdmin.fields
        # TODO: we are not using ModelAdmin.exclude but directly manipulating ModelAdmin.fields. Which is better?
        self.fields, self._exclude_fields = self.supplemental_fields.choose_fields(self.fields, obj)

    def get_exclude_fields(self, obj=None):
        if not self._exclude_fields:
            self.set_exclude_fields(obj)
        return self._exclude_fields

    def update_exclude_history(self, form_exclude, obj):
        """Updates the admin_supplemental_fields Excluded history model to remember which fields were excluded on Add.

        Also, resets form._meta.exclude.

        .. seealso:: post delete signal."""
        if self.form._meta.exclude:
            # record which instances were selected for excluded fields, (see also the post_delete signal).
            if Excluded.objects.filter(app_label=obj._meta.app_label, object_name=obj._meta.object_name, model_pk=obj.pk):
                excluded = Excluded.objects.get(app_label=obj._meta.app_label, object_name=obj._meta.object_name, model_pk=obj.pk)
                excluded.excluded = self.get_exclude_fields(obj)
                excluded.save()
            else:
                Excluded.objects.create(app_label=obj._meta.app_label, object_name=obj._meta.object_name, model_pk=obj.pk, excluded=self.get_exclude_fields(obj))
        # clear in case the form instance, or this instancem, is used again
        self.form._meta.exclude = None
        self._exclude_fields = None
