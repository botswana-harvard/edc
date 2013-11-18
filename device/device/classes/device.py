import re
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


class Device(object):

    """ Determines the device name, useful to know when identifiers are created by the device.

    Tries settings.py (with DEVICE_ID settings attribute).
    Must be a number."""

    SERVER_DEVICE_ID_LIST = [91, 92, 93, 94, 95, 96, 97, 99, 70, 71]  # reserved device ids. 70 is the Ranaka server, 71 Digawana server. DONT CHANGE, ASK ONE IF UNSURE.
    MIDDLEMAN_DEVICE_ID_LIST = [98]

    def __init__(self, device_id=None, settings_attr=None):
        self._settings_attr = settings_attr or 'DEVICE_ID'
        self._device_id = None
        self._length = None
        self._is_server = None
        self._is_middleman = None
        self.set_device_id(device_id)
        self.set_is_server()
        self.set_is_middleman()

    @property
    def device_id(self):
        return self.get_device_id()

    def get_settings_attr(self):
        return self._settings_attr

    def get_device_id(self):
        return self._device_id

    def set_device_id(self, device_id):
        self._device_id = device_id  # only passed when testing
        if not self._device_id:
            if self.get_settings_attr() not in dir(settings):
                raise ImproperlyConfigured('Cannot determine the \'device_id\' for this device. Cannot find settings attribute {0}'.format(self.get_settings_attr()))
            else:
                self._device_id = getattr(settings, self.get_settings_attr())
        if self._device_id:
            self._device_id = str(self._device_id)
            if not re.match(r'^\d+$', self._device_id):
                raise ImproperlyConfigured('Incorrect format for settings attribute {0}. Must be a number. Got {1}'.format(self.get_settings_attr(), self._device_id))
            if self._device_id.startswith('0'):
                raise ImproperlyConfigured('Incorrect format for settings attribute {0}. Cannot start with \'0\'. Got {1}'.format(self.get_settings_attr(), self._device_id))
        else:
            raise ImproperlyConfigured('Device id may not be None.')
        return self._device_id

    def set_is_server(self):
        self._is_server = False
        if int(self._device_id) in self.SERVER_DEVICE_ID_LIST:
            self._is_server = True

    def is_producer_name_server(self, name):
        if not name:
            raise TypeError('argument name cannot be None. Pass the producer name.')
        hostname = name.split('-')[0]
        if int(hostname[4:]) in self.SERVER_DEVICE_ID_LIST:
            return True
        return False
            
    def set_is_middleman(self):
        self._is_middleman = False
        if int(self._device_id) in self.MIDDLEMAN_DEVICE_ID_LIST:
            self._is_middleman = True

    def is_server(self):
        if not self._is_server:
            self.set_is_server()
        return self._is_server

    def is_middleman(self):
        if not self._is_middleman:
            self.set_is_middleman()
        return self._is_middleman
