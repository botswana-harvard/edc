from django.db import models

from utils import string_to_datatype


class ConfigurationManager(models.Manager):

    def get_attr_value(self, attribute_name):
        """Returns the attribute value in its original datatype assuming it can be converted."""
        obj = self.get(attribute=attribute_name)
        string_value = obj.value.strip(' "')
        if obj.convert:
            value = string_to_datatype(string_value)
        else:
            value = string_value
        return value
