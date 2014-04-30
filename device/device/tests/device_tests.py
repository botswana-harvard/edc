from django.test import SimpleTestCase
from django.core.exceptions import ImproperlyConfigured

from ..classes import Device


class DeviceTests(SimpleTestCase):

    def test_device1(self):
        """ Cannot start with 0 """
        self.assertRaises(ImproperlyConfigured, Device, device_id='01', settings_attr='ERIK_IS_A_DEVICE')

    def test_device2(self):
        """ must be a number not letters"""
        self.assertRaises(ImproperlyConfigured, Device, device_id='A1', settings_attr='ERIK_IS_A_DEVICE')

    def test_device3(self):
        """ must be a number without spaces"""
        self.assertRaises(ImproperlyConfigured, Device, device_id='1 ', settings_attr='ERIK_IS_A_DEVICE')

    def test_device4(self):
        """ must be a number not \'\' """
        self.assertRaises(ImproperlyConfigured, Device, device_id='', settings_attr='ERIK_IS_A_DEVICE')

    def test_device5(self):
        """ cannot be None """
        self.assertRaises(ImproperlyConfigured, Device, device_id=None, settings_attr='ERIK_IS_A_DEVICE')

    def test_device6(self):
        """ does implicit conversion to string """
        self.assertEquals(Device(device_id=5, settings_attr='ERIK_IS_A_DEVICE').device_id, '5')

    def test_device7(self):
        """ accepts a numeric string """
        self.assertEquals(Device(device_id='5', settings_attr='ERIK_IS_A_DEVICE').device_id, '5')

    def test_knows_is_server(self):
        for i in range(91, 100):
            device = Device(device_id='99', settings_attr='ERIK_IS_A_DEVICE')
            self.assertTrue(device.is_server)

    def test_knows_is_not_server(self):
        device = Device(device_id='90', settings_attr='ERIK_IS_A_DEVICE')
        self.assertFalse(device.is_server)
