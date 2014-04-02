import copy
import random

from django.core.exceptions import ImproperlyConfigured

from ..models import ExcludedHistory


class SupplementalFields(object):
    """ Excludes fields on the fly based on a given probability.

        * p is the probability the field will appear on the form; that is, will NOT be excluded from the fields attribute tuple
        * Fields are removed from the fields attribute tuple of an admin class.
        * Excluded fields are added to the form._meta.exclude tuple so that it operates correctly with the :func:clean method.
        * if the forms Meta class exclude attribute already specifies fields to exclude, an error will occur.

        For example::
            # If p=0.1, the supplemental fields will appear 100/1000 times the admin add form is shown.
            from edc.core.admin_supplemental_fields.classes import SupplementalFields

            class MyModelAdmin(model.ModelAdmin):
                form = MyForm
                supplemental_fields = SupplementalFields(('regular_sex', 'having_sex', 'having_sex_reg', ), p=0.9)
                fields = ('field0', 'field1', 'regular_sex', 'having_sex', 'having_sex_reg')
                ...
    """

    def __init__(self, supplemental_fields, p=None, group=None, grouping_field=None):
        self._fields_verified = False
        self._exclude_fields = None
        self._probability_to_include = None
        self.group = group
        self.grouping_field = None
        self.grouping_field = grouping_field
        self.grouping_pk = None  # not used?
        self.model = None  # set by ModelAdmin
        self.model_instance = None
        self.probability_to_include = p
        self.original_model_admin_fields = None
        self.retrieved_exclude_fields_from_history = False
        self.supplemental_fields = supplemental_fields  # field names that might be excluded from the ModelAdmin fields tuple

    def __repr__(self):
        return 'SupplementalFields({0.supplemental_fields!r})'.format(self)

    def __str__(self):
        return '({0.supplemental_fields!r})'.format(self)

    def choose_fields(self, instance_pk=None, model=None, model_admin_fields=None):
        """Chooses and returns tuples of fields and exclude_fields called from ModelAdmin get_form().

        model_instance may be None if calling get_form on Add.

        This is called from get_form()."""
        self.model, self.original_model_admin_fields = self.model or model, self.original_model_admin_fields or model_admin_fields  # tests will pass model and model_admin_fields
        self.check_supplemental_field_attrs()
        try:
            self.model_instance = self.model.objects.get(pk=instance_pk)
        except self.model.DoesNotExist:
            pass
        # any field listed in supplemental_fields must be in original admin fields
        self.check_supplemental_in_original()
        # exclude field names from the original model_admin fields list if exclude fields is not None
        new_model_admin_fields = tuple([fld_name for fld_name in list(self.original_model_admin_fields) if fld_name not in self.exclude_fields])
        self.create_or_update_history(instance_pk)
        return new_model_admin_fields

    def check_supplemental_in_original(self):
        """Checks for any supplemental fields not listed in original fields."""
        for supplemental_field in self.supplemental_fields:
            if supplemental_field not in self.original_model_admin_fields:
                raise AttributeError('Supplemental field \'{0}\' must be listed in fields.'.format(supplemental_field))
        return True

    @property
    def exclude_fields(self):
        """Returns a list of fields to exclude from the original fields list.

        Override this method to change how the choice is made between returning [] and supplemental_fields.
        """
        self._exclude_fields = self.exclude_fields_from_history
        if not self._exclude_fields:
            if random.choice(self.probability_as_sequence):  # either 0 or 1
                self._exclude_fields = tuple(self.supplemental_fields)
        return self._exclude_fields

    @property
    def exclude_fields_from_history(self):
        """Checks the history model and sets the exclude fields if retrieved."""
        exclude_fields = ''
        if self.grouping_field:
            exclude_fields = self.exclude_fields_from_history_by_grouping
        elif self.model_instance:
            if ExcludedHistory.objects.filter(
                    app_label=self.model._meta.app_label,
                    object_name=self.model._meta.object_name,
                    model_pk=self.model_instance.pk
                    ).exists():
                exclude_fields = ExcludedHistory.objects.get(
                    app_label=self.model._meta.app_label,
                    object_name=self.model._meta.object_name,
                    model_pk=self.model_instance.pk
                    ).excluded_fields
                exclude_fields = self.convert_to_tuple(exclude_fields)
        return exclude_fields

    def exclude_fields_from_history_by_grouping(self):
        """Retrieve by fields to exclude using the history for this grouping field and grouping pk."""
        exclude_fields = ''
        if ExcludedHistory.objects.filter(
                group=self.group,
                grouping_field=self.grouping_field,
                grouping_pk=self.grouping_pk
                ).exists():
            exclude_fields = ExcludedHistory.objects.filter(
                group=self.group,
                grouping_field=self.grouping_field,
                grouping_pk=self.grouping_pk
                ).order_by('created')[0].excluded_fields
            exclude_fields = self.convert_to_tuple(exclude_fields)
        return exclude_fields

    def create_or_update_history(self, instance_pk):
        """Updates the admin_supplemental_fields Excluded history model to remember which fields were excluded on Add.

        .. seealso:: post delete signal."""
        try:
            excluded_history = ExcludedHistory.objects.get(app_label=self.model._meta.app_label, object_name=self.model._meta.object_name, group=self.group, grouping_pk=self.grouping_pk)
            excluded_history.model_pk = instance_pk.pk
            excluded_history.save()
        except ExcludedHistory.DoesNotExist:
            ExcludedHistory.objects.create(
                app_label=self.model._meta.app_label,
                object_name=self.model._meta.object_name,
                model_pk=instance_pk.pk,
                excluded_fields=','.join(self.exclude_fields),
                group=self.group,
                grouping_field=self.grouping_field,
                grouping_pk=self.grouping_pk)

    @property
    def probability_to_include(self):
        return self._probability_to_include

    @probability_to_include.setter
    def probability_to_include(self, probability):
        """Probability to include supplemental questions.

        If p=1.0, the questions will always be included, excluded fields = [].
        If p=0.0, the questions will never be included, excluded fields = supplemental_fields."""
        if not isinstance(probability, float):
            raise AttributeError('Probability \'p\' must be a float. Got {0}.'.format(probability))
        if probability < 0 or probability > 1:
            raise AttributeError('Probability \'p\' must be greater than 0 and less than 1. Got {0}.'.format(probability))
        if len(str(probability)) > 5:
            raise AttributeError('Probability \'p\' may not have more than 3 decimal places. Got {0}.'.format(probability))
        self._probability_to_include = probability

    @property
    def probability_as_sequence(self):
        """Converts probability to a list of 0s and 1s where 1s will include the fields.

        The default, 1, is to exclude the fields from the \'fields\' list.
        If p=0.1, the list will be 900 1s and 100 0s. the fields will be excluded
        from the list approximately 900 out of 1000 times.
        """
        return ([0] * int(1000 * self.probability_to_include)) + ([1] * int(1000 - (1000 * self.probability_to_include)))

    def check_supplemental_field_attrs(self):
        """Checks supplemental fields are nullable and editable."""
        for fld in self.model._meta.fields:
            if fld.name in self.supplemental_fields:
                if not fld.null:
                    raise ImproperlyConfigured('Supplemental fields must allow nulls, field \'{1}\' does not. See model {0}.'.format(self.model._meta.object_name, fld.name))
                if not fld.editable:
                    raise ImproperlyConfigured('Supplemental fields must be \'editable\', field \'{1}\' is not. See model {0}'.format(self.model._meta.object_name, fld.name))
        return True

    def convert_to_tuple(self, fields):
        fields = fields.strip()
        if fields:
            return tuple(fields.split(','))
        return ''
