from django.core.validators import RegexValidator
from django.db import models

from edc.base.model.models import BaseUuidModel

from ..managers import ConfigurationManager


class GlobalConfiguration(BaseUuidModel):

    category = models.CharField(max_length=25)
    attribute = models.CharField(max_length=25, validators=[RegexValidator('[a-z0-9_]', 'Invalid attribute name, must be lower case separated by underscore.'), ])
    value = models.CharField(max_length=25, help_text='any string value or string representation of a value')
    convert = models.BooleanField(default=True, help_text=('If True, automatically convert string value to its datatype. '
                                                            'Type is autodetected in this order: Boolean, None, Decimal, Integer, '
                                                            'Date, Datetime otherwise String'))
    comment = models.CharField(max_length=100)
    objects = ConfigurationManager()

    class Meta:
        app_label = 'app_configuration'
