from dateutil import parser
from decimal import Decimal

from django.db import models


class ConfigurationManager(models.Manager):

    def get_attr_value(self, *kwargs):
        """Returns the attribute value in its original datatype assuming it can be converted."""
        obj = self.get(**kwargs)
        string_value = obj.value.strip(' "')
        retval = string_value
        if obj.convert:
            retval = self.convert_from_string(string_value)
        return retval

    def convert_from_string(self, string_value):
        string_value = string_value.strip(' "')
        # try to return as boolean or none
        retval = string_value
        if string_value.lower() in ['true', 'false', 'none']:
            retval = eval(string_value)
        # try to return as a decimal
        try:
            value = Decimal(string_value)
            if str(value) == string_value:
                retval = value
        except ValueError:
            pass
        # try to return as an integer
        try:
            value = int(string_value)
            if str(value) == string_value:
                retval = value
        except ValueError:
            pass
        # try to return as date
        try:
            value = parser.parse(string_value)
            if value.strftime('%Y-%m-%d') == string_value:
                retval = value
        except:
            pass
        # try to return as datetime
        try:
            value = parser.parse(string_value)
            if value.strftime('%Y-%m-%d %H:%M') == string_value:
                retval = value
        except ValueError:
            pass
        # otherwise return string value
        return retval