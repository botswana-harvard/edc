from django.test import TestCase
from django.conf import settings
from ..models import OutgoingTransaction, IncomingTransaction, MiddleManTransaction
from .factories import MiddleManTransactionFactory
from apps.bcpp_inspector.models import SubjectRequisitionInspector


class MiddleManTests(TestCase):

    def setUp(self):
        OutgoingTransaction.objects.all().delete()
        IncomingTransaction.objects.all().delete()
        MiddleManTransaction.objects.all().delete()
        
    def test_middleman_settings(self):
        if settings.MIDDLE_MAN:
            settings.MIDDLE_MAN = False
        self.assertRaises(TypeError, lambda: MiddleManTransactionFactory())

    def test_requisition_inspector(self):
        if not settings.MIDDLE_MAN:
            settings.MIDDLE_MAN = True
        wb_requisition = MiddleManTransactionFactory()#default middle man transaction is wb requisition.
        encrypted_transaction = 'enc1:::3371d76ac151258d7c34eab2b24a281bba976a8a10cd5bcb4cbacc262773ee03enc2:::oA4YcwbQQLo9//uHdUSoF0vvxy4ibXLEd/+kmv/YSHlSKN1d8GQ2boWMH5lFhcw8kLKw9yluJ/e8FrrnEaldQ6IUfYjQcqrTi3DpPmlUSjYRj3naykxWgHcUkEQ3Krvf1r9d5UaIlKTaXohTU/sz+/4yxgDdg39BiZsZqxiqUU2TyPEcFHSYTjPij3lv0my1Bu27jdyrjFVyijivvJDIpqhpB3a7+ok+yi1ovTtcAu/jY24ElxlE0uhRVq73IC/I9S96E8pOihn29LgqJj3d+AjaE5ulTPJs3q4jdWWpCgrd5Tke0yPGIfWwIwRzWp6n1ZRo6KHEmBeCOERlDjE+9I5REFj4xXzBpdvJPW99TOCh2MzyUEsyx3JuIqtI9dI8klIba6jagQwQbRjt/5PoqeOPn+I4PQ4CnXgRddarRjySP8+yOf8pfsF2BFdopjlNM+a2SETJ7Fyi0ty+rL6GoPcVNvpYz1hDYKnvW3kvL+NUwDGoDe34HGIR+BYq/ZIjnI0lQdryoLU6/tBmUv/JTm9vQLBwZ97z7SaVCQcyuFEv1qGj12BVh3ZNF9d5G1n92geO9oJjuGi3D0DYocEYPMhIi'
        tx_pk = '8da16751-05a5-11e3-856f-7cd1c3dc18e9'
        timestamp = '20130815142355618511'
        second_requisition = MiddleManTransactionFactory(tx=encrypted_transaction, tx_pk=tx_pk, timestamp=timestamp)
        self.assertTrue(SubjectRequisitionInspector.objects.all().count(),2)
        encrypted_transaction2 = 'enc1:::c9d8c5b1cf8a9c30c5c95af5cd39d6dcb3d245a621795f17d1ee19606248e287enc2:::GhF5UK7a4oSkz2Y6noGWzylMAa8iHz6abEXj7m0mhrB73BeNjqFQSYnzIfddXt526SE/uCIOemXp8s3kxjsi64AUSMJgivAQVuv9mT0ZqdVaREgD5OrBgpvGr/O/pqLQp0kpKnN+ujuAB9J6/hXDMXr01QbV7JBfZo6NGCCEVV3rGoWkHm2ANXaviHUAaa2qan3SQIJuCKB6CluSmzvKQD3ub4RMkuPw9+ZV6eJQkwa6BQ7kL7ucBmBqMfDEyHi8oeYhakXhX0kgOwwJU4SeQ5eunDUc1QVIvdDJ8EBFFxZ9oym33+rBg9BViye91hAeEPGr4z2YAxEkBWuZjjSMApAZUUNk0Z9EsPfkRQEj4uicqWH/c4ORKh6LaCcNYdvjp2XnCK2x1q+St/e7QwAN5nv1YNCiQSAWVh6mJCDCuJP6sPxtagZZr8z1ZmXhlHvdYPo3b8i2yZ5fdAMLwuPG9L0rpz/PCmRKfTb64AhMaR5IinIjW0Gtx7lm1uQbdmIvHNceGbvobgUPZNNquzlLWTCjRJK39r5G33aubN2yj5HnvFm3SMSUDyXuZouCEHG6BK2c5W1IYuZqUviJ3A9dg7WMEc3IJWk73/ECD7X0dnBZyERv/ZtJmaOWfV6j2OK0GWQsAx+nkGY42T4McGdw3qQPi77b4RXfiTlmEIBT2mMlKNuJInfPghINMuDGBYbye7keIz7MfeCznkYfn01PmVpHKOoXhjyPogymdGFEG0Q+aYpkNMiIcKIesq57sXq15VXzfx1NQ0Xg19AZoq7QfBY8Jgbmh0ktlK8J7BZjdqKJ46PBK2SOKj8QBwebWBJurrufjHuMsU89MWH5TvmJWbTOWh4KEm4ny3/C6j1opNdetbYmOcsscxgMTbjr6MizkWDDSAGtyKnW6d3J0nPPqbePaN5nsOHLtgIGZMkC681mMFQUThhJJG03ikTRWF9Jm2chuhRPvVcMSREFxPT5BOTFfIaJtETCT6RtCAud/iF/p/1MnbOFltRNzd4AP/RrJlBTojFNtdjveP7SWxh8sA==iv:::ObUcUZnbOfIm1fMCCZLx1A=='
        tx_pk2 = 'e5719544-ff68-11e2-889b-24b6fdf82a22'
        timestamp2 = '20130809152815489937'
        tx_name = 'HouseholdStructure'
        household_structure = MiddleManTransactionFactory(tx=encrypted_transaction2, tx_pk=tx_pk2, timestamp=timestamp2, tx_name=tx_name)
        self.assertTrue(SubjectRequisitionInspector.objects.all().count(),2)
        self.assertTrue(MiddleManTransaction.objects.all().count(),3)