from django.core.management.base import BaseCommand
from django.conf import settings
from meter_readings.models import Files, RegisterReadings
import os.path
from datetime import datetime


def register_readings_object(file_name, current_time, field_values):
    rr_object = RegisterReadings(
        mpan_core = field_values['mpan_core'],
        meter_id = field_values['meter_id'],
        meter_register_id = field_values['meter_register_id'],
        reading_date_time = datetime.strptime(field_values['reading_date_time'],'%Y%m%d%H%M%S'),
        register_reading = field_values['register_reading'],
        md_reset_date_time = None if field_values['md_reset_date_time'] == '' else datetime.strptime(field_values['md_reset_date_time'],'%Y%m%d%H%M%S'),
        number_of_md_resets = None if field_values['number_of_md_resets'] == '' else field_values['number_of_md_resets'],
        meter_reading_flag = True if field_values['meter_reading_flag'] == 'T' else False,
        reading_method = field_values['reading_method'],
        file_name = file_name,
        ingestion_time = current_time
    )

    return rr_object


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('file_path', nargs='?', default='')


    def handle(self, *args, **options):
        with open(options.get('file_path'),'r') as file:
            file_listified = list(file)

        file_name = os.path.basename(options.get('file_path'))
        current_time = datetime.now()

        # Proceed only when the file has not been loaded before
        existing_file = Files.objects.filter(file_name=file_name)
        if existing_file.count() > 0:
            return

        Files.objects.create(
            file_name=file_name,
            header=file_listified[0],
            footer=file_listified[-1],
            ingestion_time=current_time
        )


        object_list = []
        field_values = {}

        for i in range(1,len(file_listified)-1):
            record = file_listified[i]
            record_listified = record.split('|')

            # Repeating record for Meter/Register. Create an object using the previous Meter/Register before continuing.
            if 'meter_register_id' in field_values and record_listified[0] == '030':
                the_object = register_readings_object(file_name, current_time, field_values)
                object_list.append(the_object)

            # Repeating record for MPAN Core. Create an object with the previous record set and restart the process. 
            if 'mpan_core' in field_values and record_listified[0] == '026':
                the_object = register_readings_object(file_name, current_time, field_values)
                object_list.append(the_object)

                field_values = {}
                field_values['mpan_core'] = record_listified[1]

            # Fresh start of the flow file.
            if 'mpan_core' not in field_values and record_listified[0] == '026':
                field_values['mpan_core'] = record_listified[1]

            # Continue scanning the record set for MPAN.
            if record_listified[0] == '028':
                field_values['meter_id'] = record_listified[1]

            if record_listified[0] == '030':
                field_values['meter_register_id'] = record_listified[1]
                field_values['reading_date_time'] = record_listified[2]
                field_values['register_reading'] = record_listified[3]
                field_values['md_reset_date_time'] = record_listified[4]
                field_values['number_of_md_resets'] = record_listified[5]
                field_values['meter_reading_flag'] = record_listified[6]
                field_values['reading_method'] = record_listified[7]
            
        RegisterReadings.objects.bulk_create(object_list)