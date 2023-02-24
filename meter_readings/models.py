from django.db import models

# Create your models here.
class Files(models.Model):
    file_name = models.CharField(max_length=100)
    header = models.CharField(max_length=100)
    footer = models.CharField(max_length=100)
    ingestion_time = models.DateTimeField()

    class Meta:
        verbose_name_plural = "files"


class RegisterReadings(models.Model):
    mpan_core = models.IntegerField()
    meter_id = models.CharField(max_length=10)
    meter_register_id = models.CharField(max_length=2)
    reading_date_time = models.DateTimeField()
    register_reading = models.DecimalField(max_digits=10, decimal_places=1)
    md_reset_date_time = models.DateTimeField(null=True)
    number_of_md_resets = models.IntegerField(null=True)
    meter_reading_flag = models.BooleanField(null=True)
    reading_method = models.CharField(max_length=1)
    file_name = models.CharField(max_length=100)
    ingestion_time = models.DateTimeField()

    class Meta:
        verbose_name_plural = "register_readings"


