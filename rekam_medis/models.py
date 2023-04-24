from django.utils import timezone
from django.db import models
from daftar_terapi.models import *
from account.models import Pasien, Terapis

# Create your models here.
class RekamMedis(models.Model):
    pasien = models.ForeignKey(Pasien, on_delete=models.RESTRICT, default=0)
    terapis = models.ManyToManyField(Terapis, related_name='terapis')
    kunjungan = models.ManyToManyField(Appointment, related_name='kunjungan')

    class Meta:
        db_table = 'RekamMedis'
        
    def __str__(self):
        return 'Rekam Medis: {}'.format(self.pasien)
