from django.core.management.base import BaseCommand
from django.conf import settings
from meter_readings.models import Files, RegisterReadings
import os
import logging
logger = logging.getLogger(__name__)


file_inbox_path = settings.BASE_DIR / 'meter_readings/file_inbox/'
ingested_files_path = settings.BASE_DIR / 'meter_readings/file_inbox/ingested_files/'


class Command(BaseCommand):
    def handle(self, *args, **options):
        Files.objects.all().delete()
        RegisterReadings.objects.all().delete()

        files_count = Files.objects.all().count()
        register_readings_count = RegisterReadings.objects.all().count()
        logger.info(f'Files count :{files_count}')
        logger.info(f'RegisterReadings count: {register_readings_count}')

        paths = os.listdir(ingested_files_path)
        for path in paths:
            os.rename(ingested_files_path / path, file_inbox_path / path)