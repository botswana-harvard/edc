from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase

from ..classes import BaseUsing
from ..exceptions import UsingError, UsingSourceError, UsingDestinationError


class TestBaseUsingMethods(TestCase):
    using_source = 'default'
    using_destination = 'destination'

    def test_methods(self):
        # Base tests
        self.assertTrue('DEVICE_ID' in dir(settings), 'Settings attribute DEVICE_ID not found')

    def test_methods1(self):
        """Assert source and destination cannot be the same."""
        self.assertRaises(UsingError, BaseUsing, self.using_source, self.using_source)

    def test_methods2(self):
        """Asserts  if not provided, server_device_id defaults to 99."""
        self.assertEqual(BaseUsing(self.using_source, self.using_destination).server_device_id, '99')

    def test_methods3(self):
        """Asserts source must be either server or default."""
        self.assertRaises(UsingSourceError, BaseUsing, 'not_default', self.using_source)

    def test_methods4(self):
        """Asserts  'xdefault' is not accepted."""
        self.assertRaises(ImproperlyConfigured, BaseUsing(self.using_source, self.using_destination).is_valid_using, 'xdefault', 'source')

    def test_methods5(self):
        """Asserts accepts server_device_id as None if self.using_source is default."""
        self.assertTrue(isinstance(BaseUsing(self.using_source, self.using_destination, server_device_id=None), BaseUsing))

    def test_methods6(self):
        """Asserts if source is default, must be server = 99."""
        self.assertRaises(UsingSourceError, BaseUsing, self.using_source, self.using_destination, server_device_id='22')

    def test_methods7(self):
        """Asserts  server_device_id cannot be None if source is not default."""
        self.assertRaises(UsingSourceError, BaseUsing, 'destination', 'dispatch_destination', server_device_id=None)

    def test_methods8(self):
        """Asserts  server_device_id cannot be None if source is not default."""
        self.assertRaises(UsingSourceError, BaseUsing('server', 'dispatch_destination', server_device_id='22'))

    def test_methods9(self):
        """Asserts destination cannot be server."""
        self.assertRaises(UsingDestinationError, BaseUsing, self.using_source, 'server')
