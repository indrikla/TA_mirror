from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('pasien', 'terapis', 'tanggal_terapi', 'slot_waktu')

@admin.register(models.AppointmentStatus)
class AppointmentStatusAdmin(admin.ModelAdmin):
    list_display = ('status', 'appointment')