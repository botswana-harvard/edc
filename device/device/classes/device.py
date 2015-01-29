import re

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


class Device(object):

    """ Determines the device name, useful to know when identifiers are created by the device.

    Tries settings.py (with DEVICE_ID settings attribute).
    Must be a number."""

    SERVER_DEVICE_ID_LIST = settings.SERVER_DEVICE_ID_LIST
    MIDDLEMAN_DEVICE_ID_LIST = settings.MIDDLEMAN_DEVICE_ID_LIST

    def __str__(self):
        return self.device_id

    @property
    def device_id(self):
        try:
            device_id = str(int(settings.DEVICE_ID))
            if not device_id:
                raise ImproperlyConfigured('Device id may not be None.')
        except AttributeError:
            raise ImproperlyConfigured('Missing settings attribute DEVICE_ID. Please add to settings.py, '
                                       'e.g. DEVICE_ID = \'99\'')
        if not re.match(r'^\d+$', device_id):
            raise ImproperlyConfigured('Incorrect format for settings attribute DEVICE_ID. Must be a '
                                       'number. Got {1}'.format(device_id))
        return device_id

    @property
    def is_server(self):
        """Returns True if the device_id is is in settings.SERVER_DEVICE_ID_LIST."""
        return self.device_id in map(str, map(int, self.SERVER_DEVICE_ID_LIST))

    @property
    def is_central_server(self):
        return self.device_id == '99'

    @property
    def is_community_server(self):
        return self.device_id() in map(str, map(int, self.SERVER_DEVICE_ID_LIST)) and not self.device_id() == '99'

    @property
    def is_middleman(self):
        """Returns True if the device_id is is in settings.MIDDLEMAN_DEVICE_ID_LIST."""
        if self.MIDDLEMAN_DEVICE_ID_LIST:
            return self.device_id in map(str, map(int, self.MIDDLEMAN_DEVICE_ID_LIST))

    def is_producer_name_server(self, name):
        if not name:
            raise TypeError('argument name cannot be None. Pass the producer name.')
        hostname = name.split('-')[0]
        if hostname.find('bcpp') != -1 and int(hostname[4:]) in self.SERVER_DEVICE_ID_LIST:  # TODO: cannot refer to bcpp here!
            return True
        return False

device = Device()
