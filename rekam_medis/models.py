from django.utils import timezone
from django.db import models
from daftar_terapi.models import *
from account.models import Pasien, Terapis
import os

TIPE_CHOICES = (
    ("Fisioterapi", "Fisioterapi"),
    ("Terapi Okupasi", "Terapi Okupasi"),
    ("Terapi Wicara", "Terapi Wicara"),
)

# Create your models here.
class RekamMedis(models.Model):
    pasien = models.ForeignKey(Pasien, on_delete=models.RESTRICT, default=0)
    terapis = models.ManyToManyField(Terapis, related_name='terapis')
    kunjungan = models.ManyToManyField(Appointment, related_name='kunjungan')

    class Meta:
        db_table = 'RekamMedis'
        
    def __str__(self):
        return 'Rekam Medis: {}'.format(self.pasien)
    
    
class Asesmen(models.Model):
    pasien = models.ForeignKey(Pasien, on_delete=models.RESTRICT, default=0)
    tanggal_dibuat = models.DateField("Tanggal Dibuat", help_text="TTTT-BB-HH", default=timezone.now)
    terapis = models.ForeignKey(Terapis, on_delete=models.RESTRICT, related_name='terapis_asesmen')
    tipe = models.CharField('Tipe', null=True, blank=False, max_length=50, choices=TIPE_CHOICES)
    lampiran = models.FileField("Lampiran", upload_to='', storage=None, max_length=250, blank=True)

    class Meta:
        db_table = 'Asesmen'
        
    def __str__(self):
        return 'Asesmen: {} {}'.format(self.pasien, self.tanggal_dibuat)

    def filename(self):
        return os.path.basename(self.file.name)