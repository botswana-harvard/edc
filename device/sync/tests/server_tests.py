from django.conf import settings
from tastypie.models import ApiKey
from django.contrib.auth.models import User
from ..models import OutgoingTransaction, MiddleManTransaction
from .factories import MiddleManTransactionFactory, ProducerFactory
from .base_sync_device_tests import BaseSyncDeviceTests
from apps.bcpp_inspector.models import SubjectRequisitionInspector


class ServerTests(BaseSyncDeviceTests):

        
    def test_server_settings(self):
        if 'MIDDLE_MAN' in dir(settings) and settings.MIDDLE_MAN:
            settings.MIDDLE_MAN = False
        self.assertRaises(TypeError, lambda: MiddleManTransactionFactory())

        
    def test_tastypie_synchronizing_link(self):
        producer = 'bcpp039-bhp066'
        app_name = 'bcpp'
        producer_instance = ProducerFactory(name=producer, settings_key=producer, url='http://localhost:8000/')
        if 'MIDDLE_MAN' in dir(settings) and not settings.MIDDLE_MAN:
            settings.MIDDLE_MAN = True
        self.assertEqual(User.objects.all().count(),1)
        self.assertEqual(ApiKey.objects.all().count(),1)
        self.denies_anonymous_acess(producer, app_name)
        print 'Number of OUTGOING TRANSACTIONS = {0}'.format(OutgoingTransaction.objects.all().count())
        response = self.client.get('/bhp_sync/consume/'+producer+'/'+app_name+'/', follow=True)
        #print response
        self.assertTrue(str(response).find('/bhp_sync/api_otmr/outgoingtransaction') != -1)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response,'/dispatch/bcpp/sync/'+producer+'/')
        
