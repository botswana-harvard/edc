from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from edc_device import Device

from ..exceptions import UsingError, UsingSourceError, UsingDestinationError


class BaseUsing(object):

    def __init__(self, using_source, using_destination, server_device_id=None):
        """Initializes and verifies arguments ``using_source`` and ``using_destination``.

        Args:
            ``using_source``: settings.DATABASE key for source. Source is the server so must
                          be 'default' if running on the server and 'server'
                          if running on the device.
            ``using_destination``: settings.DATABASE key for destination. If running from the server
                               this key must exist in settings.DATABASES. If on the device, must be 'default'.
                               In either case, ``using_destination`` must be found in the
                               source :class:`Producer` model as producer.settings_key (see :func:`set_producer`.)

        Keywords:
            ``server_device_id``: settings.DEVICE_ID for server (default='99')"""
        self._using_source = None
        self._using_destination = None
        if using_source == using_destination:
            raise UsingError(
                'Arguments \'<source>\' and \'<destination\'> cannot be the '
                'same. Got \'{0}\' and \'{1}\''.format(using_source, using_destination))
        self.device = Device()
        self.server_device_id = server_device_id or self.device.central_server_id
        self.using_source = using_source
        self.using_destination = using_destination

    @property
    def using_source(self):
        """Gets the ORM `using` parameter for "source"."""
        return self._using_source

    @using_source.setter
    def using_source(self, using_source):
        """Sets the ORM `using` parameter for data access on the "source"."""
        if not using_source:
            raise UsingSourceError('Parameters \'using_source\' cannot be None')
        if using_source not in ['server', 'default']:
            raise UsingSourceError(
                'Argument \'<using_source\'> must be either \'default\' '
                '(if run from server) or \'server\' if not run from server.')
        if self.device.is_server and using_source != 'default':
            raise UsingSourceError(
                'Argument \'<using_source\'> must be \'default\' '
                'if running on the server (check settings.DEVICE).')
        if not self.device.is_server and using_source == 'default':
            raise UsingSourceError(
                'Argument \'<using_source\'> must be \'server\' '
                'if running a device (check settings.DEVICE).')
        if self.is_valid_using(using_source, 'source'):
            self._using_source = using_source

    @property
    def using_destination(self):
        """Gets the ORM `using` parameter for "destination"."""
        return self._using_destination

    @using_destination.setter
    def using_destination(self, using_destination):
        """Sets the ORM `using` parameter for data access on the "destination"."""
        if not using_destination:
            raise UsingDestinationError('Parameters \'using_destination\' cannot be None')
        if using_destination == 'server':
            raise UsingDestinationError('Argument \'<using_destination\'> cannot be \'server\'.')
        if self.device.is_server and using_destination == 'default':
            raise UsingDestinationError(
                'Argument \'<using_destination\'> cannot be \'default\' '
                'if running on the server (check settings.DEVICE).')
        if self.is_valid_using(using_destination, 'destination'):
            self._using_destination = using_destination

    def is_valid_using(self, using, label):
        """Confirms an ORM `using` parameter is valid by checking :file:`settings.py`."""
        dbKey = []
        for key in settings.DATABASES.iteritems():
            if key[0] == using:
                dbKey.append(key)
        if not dbKey:
            raise ImproperlyConfigured(
                'Cannot find {0} key \'{1}\' in settings attribute '
                'DATABASES. Please add to settings.py.'.format(using, label))
        return True
