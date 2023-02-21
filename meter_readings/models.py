from django.db import models

# Create your models here.
class Files(models.Model):
    file_name = models.CharField(max_length=100)
    header = models.CharField(max_length=100)
    footer = models.CharField(max_length=100)
    ingestion_time = models.DateTimeField()

