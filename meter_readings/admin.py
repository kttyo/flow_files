from django.contrib import admin
from .models import Files, RegisterReadings
# Register your models here.

@admin.register(Files)
class FilesAdmin(admin.ModelAdmin):
    pass

@admin.register(RegisterReadings)
class RegisterReadingsAdmin(admin.ModelAdmin):
    pass