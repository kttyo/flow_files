from django.test import TestCase
from meter_readings.models import Files, RegisterReadings
import os.path
from django.conf import settings
from django.core.management import call_command

# Create your tests here.
class DataTestCase(TestCase):
    def test_data_comparison(self):
        call_command('file_ingestion', 'meter_readings/file_inbox/DTC5259515123502080915D0010.uff')
        data_count = RegisterReadings.objects.all().count()
        self.assertEqual(data_count,13)