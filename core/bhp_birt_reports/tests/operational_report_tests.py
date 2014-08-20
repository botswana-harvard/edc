from datetime import date

from django.test import TestCase

from ..classes import OperationalReportUtilities


class OperationalReportTests(TestCase):

    def setUp(self):
        pass

    def test_date_format(self):
        utilities = OperationalReportUtilities()
        self.assertEqual(utilities.date_format_utility('YYYY/MM/DD', '2013/10/15'), date(2013,10,15))
        self.assertEqual(utilities.date_format_utility('', '2013/10/15'), date(2013,10,15))
        self.assertEqual(utilities.date_format_utility('2013-11-15', '2013/10/15'), date(2013,11,15))
        self.assertEqual(utilities.date_format_utility('2013/11/17', '2013/10/15'), date(2013,11,17))
        self.assertRaises(TypeError, utilities.date_format_utility, '2013:11:17', '2013/10/15')

