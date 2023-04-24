from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.RekamMedis)
class RekamMedisAdmin(admin.ModelAdmin):
    list_display = ('id', 'pasien')