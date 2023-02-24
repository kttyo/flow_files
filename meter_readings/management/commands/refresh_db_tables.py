from django.core.management.base import BaseCommand
from meter_readings.models import Files, RegisterReadings


class Command(BaseCommand):
    def handle(self, *args, **options):
        Files.objects.all().delete()
        RegisterReadings.objects.all().delete()

        files_count = Files.objects.all().count()
        register_readings_count = RegisterReadings.objects.all().count()
        print(f'Files count :{files_count}', f'RegisterReadings count: {register_readings_count}')