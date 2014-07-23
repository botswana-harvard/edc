import copy
import random
from ..models import ExcludedHistory


class SupplementalFields(object):
    """ Excludes fields on the fly based on a given probability.

        * p is the probability the field will appear on the form; that is, will NOT be excluded from the fields attribute tuple
        * Fields are removed from the fields attribute tuple of an admin class.
        * Excluded fields are added to the form._meta.exclude tuple so that it operates correctly with the :func:clean method.
        * if the forms Meta class exclude attribute already specifies fields to exclude, an error will occur.

        For example::
            # If p=0.1, the supplemental fields will appear 100/1000 times the admin add form is shown.
            from core.admin_supplemental_fields.classes import SupplementalFields

            class MyModelAdmin(model.ModelAdmin):
                form = MyForm
                supplemental_fields = SupplementalFields(('regular_sex', 'having_sex', 'having_sex_reg', ), p=0.9)
                fields = ('field0', 'field1', 'regular_sex', 'having_sex', 'having_sex_reg')
                ...
    """

    def __init__(self, supplemental_fields, p=None, group=None, grouping_field=None):
        self._original_model_admin_fields = None
        self._supplemental_fields = None
        self._exclude_fields = None
        self._model_inst = None
        self._model = None
        self._group = None
        self._grouping_pk = None
        self._grouping_field = None
        self._fields_verified = False
        self._probability_to_include = None
        self._retrieved_exclude_fields_from_history = False
        self.set_probability_to_include(p)
        self.set_group(group)
        self.set_grouping_field(grouping_field)
        self.set_supplemental_fields(supplemental_fields)

    def choose_fields(self, model_admin_fields, model, object_id):
        """Chooses and returns tuples of fields and exclude_fields called from ModelAdmin get_form().

        model_inst may be None if calling get_form on Add.

        This is called from get_form()."""
        self.set_model(model)
        self.check_supplemental_field_attrs()
        self.set_model_inst(object_id)
        # save the original ModelAdmin field list with this instance before it is altered
        self.set_original_model_admin_fields(model_admin_fields)
        # any field listed in supplemental_fields must be in original admin fields
        self.check_supplemental_in_original()
        # get the list of field names to add to the exclude list
        # either choose or retrieve from history
        self.set_exclude_fields()
        # exclude field names from the original model_admin fields list if exclude fields is not None
        new_model_admin_fields = tuple([fld_name for fld_name in list(self.get_original_model_admin_fields()) if fld_name not in self.get_exclude_fields()])
        return new_model_admin_fields, self.get_exclude_fields()

    def set_model_inst(self, object_id):
        if object_id:
            self._model_inst = self.get_model().objects.get(pk=object_id)

    def get_model_inst(self):
        return self._model_inst

    def set_supplemental_fields(self, supplemental_fields):
        if not supplemental_fields:
            raise AttributeError('Attribute \'{0}\' may not be None. See {0}.'.format(self))
        if not isinstance(supplemental_fields, (list, tuple)):
            raise AttributeError('Attribute \'{0}\' must be a tuple of field names. Got {0}'.format(supplemental_fields))
        self._supplemental_fields = supplemental_fields

    def get_supplemental_fields(self):
        """Returns a list of supplemental fields, that is, field names that might be excluded from the ModelAdmin fields tuple."""
        return self._supplemental_fields

    def set_original_model_admin_fields(self, original_model_admin_fields):
        """Save the original fields tuple from the ModelAdmin instance.

        ... note:: the list of fields from ModelAdmin is not necessarily the same as the list of fields from the model instance."""
        self._original_model_admin_fields = copy.deepcopy(original_model_admin_fields)

    def get_original_model_admin_fields(self):
        return self._original_model_admin_fields

    def check_supplemental_in_original(self):
        """Checks for any supplemental fields not listed in original fields."""
        for supplemental_field in self.get_supplemental_fields():
            if supplemental_field not in self.get_original_model_admin_fields():
                raise AttributeError('Supplemental field \'{0}\' must be listed in fields.'.format(supplemental_field))
        return True

    def set_exclude_fields(self):
        """Sets a list of fields to exclude from the original fields list.

        Override this method to change how the choice is made between returning [] and supplemental_fields.
        """
        self._exclude_fields = self.retrieve_exclude_fields_from_history()
        if not self.are_retrieved_from_history():
            if random.choice(self.get_probability_as_sequence()):  # either 0 or 1
                self._exclude_fields = tuple(self.get_supplemental_fields())

    def get_exclude_fields(self):
        return self._exclude_fields

    def set_group(self, value):
        self._group = value

    def get_group(self):
        return self._group

    def set_grouping_field(self, value):
        self._grouping_field = value

    def get_grouping_field(self):
        return self._grouping_field

    def set_grouping_pk(self, value):
        self._grouping_pk = value

    def get_grouping_pk(self):
        return self._grouping_pk

    def set_model(self, value):
        self._model = value

    def get_model(self):
        return self._model

    def set_probability_to_include(self, probability):
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

    def get_probability_to_include(self):
        return self._probability_to_include

    def get_probability_as_sequence(self):
        """Converts probability to a list of 0s and 1s where 1s will include the fields.

        The default, 1, is to exclude the fields from the \'fields\' list.
        If p=0.1, the list will be 900 1s and 100 0s. the fields will be excluded
        from the list approximately 900 out of 1000 times.
        """
        return ([0] * int(1000 * self.get_probability_to_include())) + ([1] * int(1000 - (1000 * self.get_probability_to_include())))

    def set_retrieved_exclude_fields_from_history(self, value):
        self._retrieved_exclude_fields_from_history = value

    def are_retrieved_from_history(self):
        return self._retrieved_exclude_fields_from_history

    def convert_to_tuple(self, fields):
        fields = fields.strip()
        if fields:
            return tuple(fields.split(','))
        return ''

    def retrieve_exclude_fields_from_history(self):
        """Checks the history model and sets the exclude fields if retrieved."""
        self.set_retrieved_exclude_fields_from_history(False)
        fields_to_exclude = ''
        if self.get_grouping_field():
            fields_to_exclude = self.retrieve_exclude_fields_from_history_by_grouping()
        if not self.are_retrieved_from_history():
            if self.get_model_inst():
                if ExcludedHistory.objects.filter(
                        app_label=self.get_model()._meta.app_label,
                        object_name=self.get_model()._meta.object_name,
                        model_pk=self.get_model_inst().pk
                        ).exists():
                    fields_to_exclude = ExcludedHistory.objects.get(
                        app_label=self.get_model()._meta.app_label,
                        object_name=self.get_model()._meta.object_name,
                        model_pk=self.get_model_inst().pk
                        ).excluded_fields
                    fields_to_exclude = self.convert_to_tuple(fields_to_exclude)
                    self.set_retrieved_exclude_fields_from_history(True)
        return fields_to_exclude

    def retrieve_exclude_fields_from_history_by_grouping(self):
        """Retrieve by fields to exclude using the history for this grouping field and grouping pk."""
        fields_to_exclude = ''
        if ExcludedHistory.objects.filter(
                group=self.get_group(),
                grouping_field=self.get_grouping_field(),
                grouping_pk=self.get_grouping_pk()
                ).exists():
            fields_to_exclude = ExcludedHistory.objects.filter(
                group=self.get_group(),
                grouping_field=self.get_grouping_field(),
                grouping_pk=self.get_grouping_pk()
                ).order_by('created')[0].excluded_fields
            fields_to_exclude = self.convert_to_tuple(fields_to_exclude)
            self.set_retrieved_exclude_fields_from_history(True)
        return fields_to_exclude

    def check_supplemental_field_attrs(self):
        """Checks supplemental fields are nullable and editable."""
        for fld in self.get_model()._meta.fields:
            if fld.name in self.get_supplemental_fields():
                if not fld.null:
                    raise AttributeError('Supplemental fields must allow nulls, field \'{1}\' does not. See model {0}.'.format(self.get_model()._meta.object_name, fld.name))
                if not fld.editable:
                    raise AttributeError('Supplemental fields must be \'editable\', field \'{1}\' is not. See model {0}'.format(self.get_model()._meta.object_name, fld.name))
        return True
