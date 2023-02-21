from django.contrib import admin
from .models import Files, RegisterReadings
# Register your models here.

@admin.register(Files)
class FilesAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'header', 'footer', 'ingestion_time')
    search_fields = ['file_name']
    
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(RegisterReadings)
class RegisterReadingsAdmin(admin.ModelAdmin):
    list_display = ('mpan_core', 'meter_id', 'meter_register_id', 'reading_date_time', 'register_reading', 'md_reset_date_time', 'number_of_md_resets', 'meter_reading_flag', 'reading_method', 'file_name', 'ingestion_time')
    search_fields = ['mpan_core', 'meter_id', 'file_name', 'ingestion_time']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False