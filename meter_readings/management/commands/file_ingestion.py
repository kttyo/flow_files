from django.core.management.base import BaseCommand
from django.conf import settings
from meter_readings.models import Files, RegisterReadings
import os.path
from datetime import datetime


def rr_object(mpan_cores, meter_reading_type, register_readings, file_name, ingestion_time):
    new_object = RegisterReadings(
        # Data from MPAN Cores
        mpan_core = mpan_cores[1],

        # Data from Meter/Reading Types
        meter_id = meter_reading_type[1],

        # Data from Register Readings
        meter_register_id = register_readings[1],
        reading_date_time = datetime.strptime(register_readings[2],'%Y%m%d%H%M%S'),
        register_reading = float(register_readings[3]),
        md_reset_date_time = None if register_readings[4] == '' else datetime.strptime(register_readings[4],'%Y%m%d%H%M%S'),
        number_of_md_resets = None if register_readings[5] == '' else register_readings[5],
        meter_reading_flag = True if register_readings[6] == 'T' else False,
        reading_method = register_readings[7],
        file_name = file_name,
        ingestion_time = ingestion_time
    )

    return new_object


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('file_path', nargs='?', default='')


    def handle(self, *args, **options):
        with open(options.get('file_path'),'r') as file:
            file_listified = list(file)

        file_name = os.path.basename(options.get('file_path'))
        ingestion_time = datetime.now()

        # Proceed only when the file has not been loaded before
        existing_file = Files.objects.filter(file_name=file_name)
        if existing_file.count() > 0:
            print('The file you requested to ingest is already present in the database.')
            return

        Files.objects.create(
            file_name=file_name,
            header=file_listified[0],
            footer=file_listified[-1],
            ingestion_time=ingestion_time
        )


        object_list = []
        mpan_cores = []
        meter_reading_type = []
        register_readings = []

        prev_record_type = '000'

        for line in file_listified:
            line_listified = line.split('|')

            # Skip header
            if line_listified[0] > '999' and not mpan_cores:
                continue

            # Create object and append it to object_list when a record set ends or footer appers
            if line_listified[0] <= prev_record_type or line_listified[0] > '999':
                new_rr_object = rr_object(mpan_cores, meter_reading_type, register_readings, file_name, ingestion_time)
                object_list.append(new_rr_object)

            # Fresh start of the flow file.
            if line_listified[0] == '026':
                mpan_cores = line_listified

            # Continue scanning the record set for MPAN.
            if line_listified[0] == '028':
                meter_reading_type = line_listified

            if line_listified[0] == '030':
                register_readings = line_listified
            
            prev_record_type = line_listified[0]
            
        RegisterReadings.objects.bulk_create(object_list)