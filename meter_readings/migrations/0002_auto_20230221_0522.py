# Generated by Django 3.2 on 2023-02-21 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meter_readings', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registerreadings',
            name='md_reset_date_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='registerreadings',
            name='meter_reading_flag',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='registerreadings',
            name='number_of_md_resets',
            field=models.IntegerField(null=True),
        ),
    ]
