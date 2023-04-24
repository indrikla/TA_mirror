from django.utils import timezone
from django.db import models
from account import models as account_models

# Create your models here.
class Appointment(models.Model):

    TIMESLOT_LIST = (
        ('09:00', '09:00'),
        ('10:00', '10:00'),
        ('11:00', '11:00'),
        ('13:00', '13:00'),
        ('14:00', '14:00'),
        ('15:00', '15:00')
    )

    STATUS_CHOICES = (
        (0, "Menunggu Konfirmasi"),
        (1, "Dikonfirmasi"),
        (2, "Sedang Berlangsung"),
        (3, "Menunggu Pembayaran"),
        (4, "Selesai"),
        (5, "Menunggu Pembatalan"),
        (6, "Dibatalkan"),
        (7, "Tidak Hadir"),
    )

    METODE_PEMBAYARAN_CHOICES = (
        ("Tunai", "Tunai"),
        ("Transfer", "Transfer"),
        ("QRIS", "QRIS")
    )

    pasien = models.ForeignKey(account_models.Pasien, on_delete=models.RESTRICT, default=0)
    terapis = models.ForeignKey(account_models.Terapis, on_delete=models.RESTRICT, default=0)
    keluhan_utama = models.TextField("Keluhan Utama", max_length=500)
    durasi_keluhan = models.CharField("Durasi Keluhan", max_length=50)
    perjalanan_keluhan = models.TextField("Perjalanan Keluhan", max_length=500)
    aktivitas_fisik = models.CharField("Aktivitas Fisik", max_length=100)
    pemeriksaan_penunjang = models.FileField("Pemeriksaan Penunjang", upload_to='', storage=None, max_length=250, blank=True)
    tanggal_terapi = models.DateField("Tanggal Terapi", help_text="TTTT-BB-HH", default=timezone.now)
    slot_waktu = models.CharField("Slot Waktu", max_length=50, choices=TIMESLOT_LIST)
    kunjungan_ke = models.IntegerField("Kunjungan ke", default=0)
    waktu_mulai = models.TimeField("Waktu Mulai")
    waktu_selesai = models.TimeField("Waktu Selesai")
    status = models.IntegerField("Status", choices=STATUS_CHOICES)
    catatan_terapis = models.CharField("Catatan Terapis", max_length=500, blank=True, default="")
    alasan_batal = models.CharField("Alasan Batal", max_length=250, blank=True, default="")
    pemeriksaan = models.TextField("Pemeriksaan", max_length=500, blank=True, default="")
    tindakan = models.TextField("Tindakan", max_length=500, blank=True, default="")
    evaluasi_terapi = models.TextField("Evaluasi Terapi", max_length=500, blank=True, default="")
    catatan_terapi = models.TextField("Catatan Terapi", max_length=500, blank=True, default="")
    verifikasi = models.BooleanField("Verifikasi Rekam Medis", default=False)
    nominal_pembayaran = models.CharField("Nominal Pembayaran", max_length=50, blank=True, default="")
    metode_pembayaran = models.CharField("Cara Pembayaran", max_length=10, choices=METODE_PEMBAYARAN_CHOICES, default="")

    class Meta:
        db_table = 'Appointment'

    def __str__(self):
        return '{} {} {}. Patient: {}'.format(self.tanggal_terapi, self.slot_waktu, self.terapis, self.pasien)

class AppointmentStatus(models.Model):
    class StatusChoices(models.TextChoices):
        MENUNGGU_KONFIRMASI = "0", "Menunggu Konfirmasi"
        DIKONFIRMASI = "1", "Dikonfirmasi"
        MENUNGGU_PEMBATALAN = "2", "Menunggu Pembatalan"
        DIBATALKAN = "3", "Dibatalkan"
        SEDANG_BERLANGSUNG = "4", "Sedang Berlangsung"
        TIDAK_HADIR = "5", "Tidak Hadir"
        MENUNGGU_PEMBAYARAN = "6", "Menunggu Pembayaran"
        SELESAI = "7", "Selesai"
    
    status = models.CharField(
        max_length=25,
        choices=StatusChoices.choices,
        default=StatusChoices.MENUNGGU_KONFIRMASI
    )

    appointment = models.ForeignKey(
        'Appointment', related_name="appointment_status", on_delete=models.CASCADE, null=True
    )

    def __str__(self):
        return f'AppointmentStatus {self.pk} - {self.status}'