import re

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


class Device(object):

    """ Determines the device name, useful to know when identifiers are created by the device.

    Tries settings.py (with DEVICE_ID settings attribute).
    Must be a number."""

    SERVER_DEVICE_ID_LIST = settings.SERVER_DEVICE_ID_LIST
    MIDDLEMAN_DEVICE_ID_LIST = settings.MIDDLEMAN_DEVICE_ID_LIST

    def __init__(self, device_id=None, settings_attr=None):
        self._device_id = None
        self._length = None
        self.settings_attr = settings_attr or 'DEVICE_ID'
        self.device_id = device_id

    @property
    def device_id(self):
        return self._device_id

    @device_id.setter
    def device_id(self, device_id):
        self._device_id = device_id
        if not self._device_id:
            if self.settings_attr not in dir(settings):
                raise ImproperlyConfigured('Cannot determine the \'device_id\' for this device. Cannot find settings attribute {0}'.format(self.settings_attr))
            else:
                self._device_id = getattr(settings, self.settings_attr)
        if self._device_id:
            self._device_id = str(self._device_id)
            if not re.match(r'^\d+$', self._device_id):
                raise ImproperlyConfigured('Incorrect format for settings attribute {0}. Must be a number. Got {1}'.format(self.settings_attr, self._device_id))
            if self._device_id.startswith('0'):
                raise ImproperlyConfigured('Incorrect format for settings attribute {0}. Cannot start with \'0\'. Got {1}'.format(self.settings_attr, self._device_id))
        else:
            raise ImproperlyConfigured('Device id may not be None.')
        return self._device_id

    @property
    def is_server(self):
        return int(self.device_id) in self.SERVER_DEVICE_ID_LIST

    @property
    def is_middleman(self):
        return int(self.device_id) in self.MIDDLEMAN_DEVICE_ID_LIST

    def is_producer_name_server(self, name):
        if not name:
            raise TypeError('argument name cannot be None. Pass the producer name.')
        hostname = name.split('-')[0]
        if hostname.find('bcpp') != -1 and int(hostname[4:]) in self.SERVER_DEVICE_ID_LIST:  # TODO: cannot refer to bcpp here!
            return True
        return False
