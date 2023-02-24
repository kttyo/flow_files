from django.test import TestCase
from meter_readings.models import RegisterReadings
from django.core.management import call_command
import os


# Create your tests here.
class DataTestCase(TestCase):
    def test_data_comparison(self):
        with open('./meter_readings/file_inbox/DTC5259515123502080915D0010.uff', 'r') as file:
            file_listified = file.readlines()
        
        count_rr_record = 0
        for line in file_listified:
            if line.split('|')[0] == '030':
                count_rr_record += 1
        call_command('file_ingestion', './meter_readings/file_inbox/DTC5259515123502080915D0010.uff')
        os.rename(
            './meter_readings/file_inbox/imported_files/DTC5259515123502080915D0010.uff',
            './meter_readings/file_inbox/DTC5259515123502080915D0010.uff'
            )
        data_count = RegisterReadings.objects.all().count()
        self.assertEqual(data_count,count_rr_record)