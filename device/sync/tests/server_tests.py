import socket
from django.conf import settings
from tastypie.models import ApiKey
from django.contrib.auth.models import User
from ..models import OutgoingTransaction, MiddleManTransaction
from .factories import MiddleManTransactionFactory, ProducerFactory
from .base_sync_device_tests import BaseSyncDeviceTests
from apps.bcpp_inspector.models import SubjectRequisitionInspector


class ServerTests(BaseSyncDeviceTests):

        
    def test_server_settings(self):
        if 'MIDDLE_MAN' in dir(settings):
            settings.MIDDLE_MAN = False
        self.assertTrue(settings.DEVICE_ID == '99')
       
    def test_tastypie_synchronizing_link(self):
        producer = 'bcpp039-bhp066'
        app_name = 'bcpp'
        producer_instance = ProducerFactory(name=producer, settings_key=producer, url='http://localhost:8000/')
        if 'MIDDLE_MAN' in dir(settings):
            settings.MIDDLE_MAN = False
        self.assertEqual(User.objects.all().count(),1)
        self.assertEqual(ApiKey.objects.all().count(),1)
        self.denies_anonymous_acess(producer, app_name)
        print 'Number of OUTGOING TRANSACTIONS = {0}'.format(OutgoingTransaction.objects.all().count())        
        #print response
        if not socket.gethostname()+'-bhp066' in settings.MIDDLE_MAN_LIST:
            response = self.client.get('/bhp_sync/consume/'+producer+'/'+app_name+'/', follow=True)
            self.assertTrue(str(response).find('/bhp_sync/api_otsr/outgoingtransaction') != -1)
            self.assertFalse(str(response).find('/bhp_sync/api_mmtr/middlemantransaction') != -1)           
        elif socket.gethostname()+'-bhp066' in settings.MIDDLE_MAN_LIST:
            settings.MIDDLE_MAN_LIST.append(socket.gethostname()+'-bhp066')
            response = self.client.get('/bhp_sync/consume/'+producer+'/'+app_name+'/', follow=True)
            self.assertTrue(str(response).find('/bhp_sync/api_mmtr/middlemantransaction') != -1)
            self.assertFalse(str(response).find('/bhp_sync/api_otsr/outgoingtransaction') != -1)     
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response,'/dispatch/bcpp/sync/'+producer+'/')
        
