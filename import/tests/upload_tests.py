from datetime import date, timedelta
from django.test import TestCase
from .factories import UploadSkipDaysFactory, UploadTransactionFileFactory
from ..models import UploadSkipDays, UploadTransactionFile


class UploadTests(TestCase):

    def setUp(self):
        pass
        
    def test_create_initial_skip(self):
        self.assertEqual(UploadSkipDays.objects.count(), 0)
        skip_day = UploadSkipDaysFactory(skip_date = date.today() - timedelta(1))
        self.assertEqual(UploadSkipDays.objects.count(), 1)
        UploadSkipDays.objects.all()[0].delete()
          
    def test_initial_upload_file(self):
        self.assertEqual(UploadTransactionFile.objects.count(), 0)
        upload_file = UploadTransactionFileFactory(file_name='bcpp_ranaka_201311191820.json')
        self.assertEqual(UploadTransactionFile.objects.count(), 1)
        UploadTransactionFile.objects.count()[0].delete()
    
    def test_skip_upload_logic(self):
        #Ensure that you initially have zero uploaded transaction files.
        self.assertEqual(UploadTransactionFile.objects.count(), 0)
        #Ensure that you initially have zero skip days defined
        self.assertEqual(UploadSkipDays.objects.count(), 0)
        #create initial upload file, all should work ok.
        upload_file_1 = UploadTransactionFileFactory(file_name='bcpp_ranaka_201311191820.json', identifier='ranaka')
        #Attempting to create another upload file for the same day and identifier(ranaka) should raise an error.
        self.assertRaises(TypeError, UploadTransactionFileFactory(file_name='bcpp_ranaka_201311191820.json', identifier='ranaka'))
        #Creating another upload file with a different identifier(digawana) should work fine
        upload_file_2 = UploadTransactionFileFactory(file_name='bcpp_digawana_201311191820.json', identifier='digawana')
        #Attempting to create a skip day for an identifier(ranaka) with an existing upload file should raise an error.
        self.assertRaises(TypeError, UploadSkipDaysFactory(identifier='ranaka'))
        #creating the next day as a skip day for ranaka should be ok.
        skip_day_1 = UploadSkipDaysFactory(skip_date=date(2013,11,20) + timedelta(1), identifier='ranaka')
        #Attempting to create another upload two days from now for digawana should fail i.e no previous day upload or skip day found.
        self.assertRaises(TypeError, UploadTransactionFileFactory(file_name='bcpp_ranaka_201311211820.json', identifier='digawana'))
        #Creating an upload for two days later for ranaka should work as there is a skip day from previous day.
        UploadTransactionFileFactory(file_name='bcpp_ranaka_201311211820.json', identifier='ranaka')
        #Attempting to create a skip day for two days later for digawana should fail i.e no previous date skip or upload
        self.assertRaises(TypeError, UploadSkipDaysFactory(skip_date=date(2013,11,20) + timedelta(2), identifier='digawana'))
        #Creating an upload for three days later for ranaka should work as there is an upload day from previous day.
        UploadTransactionFileFactory(file_name='bcpp_ranaka_201311221820.json', identifier='ranaka')
        
        
