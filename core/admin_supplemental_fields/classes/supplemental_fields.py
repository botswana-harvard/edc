import copy
import random
from ..models import Excluded


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

    def __init__(self, supplemental_fields, p=None, group=None):
        #TODO: handle group
        self._original_model_admin_fields = None
        self._supplemental_fields = None
        self._model_inst = None
        self._fields_verified = False
        self._set_probability(p)
        self._set_supplemental_fields(supplemental_fields)

    def _set_model_inst(self, model_inst):
        # supplemental_fields must be nullable and editable
        self._check_supplemental_field_attrs(model_inst)
        self._model_inst = model_inst

    def _get_model_inst(self):
        return self._model_inst

    def choose_fields(self, model_admin_fields, model_inst):
        """Chooses and returns tuples of fields and exclude_fields called from ModelAdmin get_form().

        This is called from get_form()."""
        self._set_model_inst(model_inst)
        # save the original ModelAdmin field list with this instance before it is altered
        self._set_original_model_admin_fields(model_admin_fields)
        # any field listed in supplimental_fields must be in original admin fields
        # TODO: this should be checked when the ModelAdmin is instantiated
        self._check_supplemental_in_original()
        # get the list of field names to add to the exclude list
        # either choose or retrieve from history
        exclude_fields = self._get_exclude_fields(model_inst)
        # exclude field names from the original model_admin fields list if exclude fields is not None
        new_model_admin_fields = tuple([fld_name for fld_name in list(self._get_original_model_admin_fields()) if fld_name not in exclude_fields])
        return new_model_admin_fields, exclude_fields

    def _set_supplemental_fields(self, supplemental_fields):
        if not supplemental_fields:
            raise AttributeError('Attribute \'{0}\' may not be None. See {0}.'.format(self))
        if not isinstance(supplemental_fields, (list, tuple)):
            raise AttributeError('Attribute \'{0}\' must be a tuple of field names. Got {0}'.format(supplemental_fields))
        self._supplemental_fields = supplemental_fields

    def _get_supplemental_fields(self):
        """Returns a list of supplemental fields, that is, field names that might be excluded from the ModelAdmin fields tuple."""
        return self._supplemental_fields

    def _set_original_model_admin_fields(self, original_model_admin_fields):
        """Save the original fields tuple from the ModelAdmin instance.

        ... note:: the list of fields from ModelAdmin is not necessarily the same as the list of fields from the model instance."""
        self._original_model_admin_fields = copy.deepcopy(original_model_admin_fields)

    def _get_original_model_admin_fields(self):
        return self._original_model_admin_fields

    def _check_supplemental_in_original(self):
        """Checks for any supplemental fields not listed in original fields."""
        for supplemental_field in self._get_supplemental_fields():
            if supplemental_field not in self._get_original_model_admin_fields():
                raise AttributeError('Supplemental field \'{0}\' must be listed in fields.'.format(supplemental_field))
        return True

    def _get_exclude_fields(self, model_inst):
        """Sets and returns a list of fields to exclude from the original fields list.

        The return value is either an empty list or the list of supplemental_fields.

        Override this method to change how the choice is made between returning [] and supplemental_fields.
        """
        exclude_fields = []
        if model_inst:
            exclude_fields = self._retrieve_fields_to_exclude(model_inst)
        else:
            exclude_fields = self._choose_fields_to_exclude()
        return exclude_fields

    def _set_probability(self, probability):
        if not isinstance(probability, float):
            raise AttributeError('Probability \'p\' must be a float. Got {0}.'.format(probability))
        if probability < 0 or probability > 1:
            raise AttributeError('Probability \'p\' must be greater than 0 and less than 1. Got {0}.'.format(probability))
        if len(str(probability)) > 5:
            raise AttributeError('Probability \'p\' may not have more than 3 decimal places. Got {0}.'.format(probability))
        self._probability = probability

    def _get_probability(self):
        return self._probability

    def _get_probability_as_sequence(self):
        """Converts probability to a list of 0s and 1s where 1s will include the fields.

        The default, 1, is to exclude the fields from the \'fields\' list.
        If p=0.1, the list will be 900 1s and 100 0s. the fields will be excluded
        from the list approximately 900 out of 1000 times.
        """
        return ([0] * int(1000 * self._get_probability())) + ([1] * int(1000 - (1000 * self._get_probability())))

    def _choose_fields_to_exclude(self):
        """Chooses to return the list of fields to exclude based on the probablity.

        The list of fields to exclude is either [] or the supplemental field list."""
        exclude_fields = []
        if random.choice(self._get_probability_as_sequence()):  # either 0 or 1
            exclude_fields = tuple(self._get_supplemental_fields())
        return exclude_fields

    def _retrieve_fields_to_exclude(self, model_inst):
        exclude_fields = []
        if not model_inst:
            raise AttributeError('Attribute \'obj\' cannot be None.')
        # you are editing, lookup the choice that was used to create obj.
        # Instances are only logged if exclude fields is not null
        # Instances are logged in :func:`base_model_admin.save_model`
        if Excluded.objects.filter(app_label=model_inst._meta.app_label, object_name=model_inst._meta.object_name, model_pk=model_inst.pk).exists():
            exclude_fields = self._get_supplemental_fields()
        return exclude_fields

    def _check_supplemental_field_attrs(self, model_inst):
        """Checks supplemental fields are nullable and editable."""
        for fld in model_inst._meta.fields:
            if fld.name in self._get_supplemental_fields():
                if not fld.null:
                    raise AttributeError('Supplemental fields must allow nulls, field \'{1}\' does not. See model {0}.'.format(model_inst._meta.object_name, fld.name))
                if not fld.editable:
                    raise AttributeError('Supplemental fields must be \'editable\', field \'{1}\' is not. See model {0}'.format(model_inst._meta.object_name, fld.name))
        return True
