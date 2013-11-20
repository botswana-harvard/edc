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
        upload_file_1 = UploadTransactionFileFactory(identifier='file1')
        #Attempting to create another upload file for the same day and identifier(community) should raise an error.
        self.assertRaises(TypeError, UploadTransactionFileFactory(identifier='file1'))
        #Creating another upload file with a different identifier(community) should work fine
        upload_file_2 = UploadTransactionFileFactory(identifier='file2')
        #Attempting to create a skip day for an identifier(community) with an existing upload file should raise an error.
        self.assertRaises(TypeError, UploadSkipDaysFactory(identifier='file1'))
        #creating the next day as a skip day for FILE1 should be ok.
        skip_day_1 = UploadSkipDaysFactory(skip_date=date.today() + timedelta(1), identifier='file1')
        #Attempting to create another upload two days from now for FILE2 should fail i.e no previous day upload or skip day found.
        self.assertRaises(TypeError, UploadTransactionFileFactory(file_date=date.today() + timedelta(2), identifier='file2'))
        #Creating an upload for two days later for FILE1 should work as there is a skip day from previous day.
        UploadTransactionFileFactory(file_date=date.today() + timedelta(2), identifier='file1')
        #Attempting to create a skip day for two days later for FILE2 should fail i.e no previous date skip or upload
        self.assertRaises(TypeError, UploadSkipDaysFactory(file_date=date.today() + timedelta(2), identifier='file2'))
        #Creating an upload for three days later for FILE1 should work as there is an upload day from previous day.
        UploadTransactionFileFactory(file_date=date.today() + timedelta(3), identifier='file1')
        
        
