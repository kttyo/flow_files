from datetime import datetime
import os
import os.path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone

from meter_readings.models import Files, RegisterReadings


file_inbox_path = settings.BASE_DIR / 'meter_readings/file_inbox/'
imported_files_path = settings.BASE_DIR / 'meter_readings/file_inbox/imported_files/'

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


def create_rr_object(file_listified, ingestion_time, file_name):
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
    try:    
        RegisterReadings.objects.bulk_create(object_list)
    except Exception as e:
        print(e)
    else:
        os.rename(file_inbox_path / file_name, imported_files_path / file_name)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('file_name', nargs='?', default='')


    def handle(self, *args, **options):
        ingestion_time = timezone.now()

        # By default, all .uff files in the inbox are targeted for processing
        paths = os.listdir(file_inbox_path)
        uff_files = [path for path in paths if path.endswith('.uff')]

        # If file name is passed as a command argument, only that file gets processed
        if options.get('file_name'):
            uff_files = [options.get('file_name')]

        for file_name in uff_files:    
            try:
                with open(file_inbox_path / file_name,'r') as file:
                    file_listified = list(file)
            except Exception as e:
                print(e)

            # Proceed only when the file has not been loaded before
            existing_file = Files.objects.filter(file_name=file_name)
            if existing_file.count() > 0:
                print('The file you requested to ingest is already present in the database.')
                return
            
            # Insert into files table
            Files.objects.create(
                file_name=file_name,
                header=file_listified[0],
                footer=file_listified[-1],
                ingestion_time=ingestion_time
            )

            # Bulk-insert into register_readings table
            create_rr_object(file_listified, ingestion_time, file_name)