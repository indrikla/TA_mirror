# Generated by Django 4.1.6 on 2023-04-20 14:38

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0002_pasien_tipe_alter_user_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keluhan_utama', models.TextField(max_length=500, verbose_name='Keluhan Utama')),
                ('durasi_keluhan', models.CharField(max_length=50, verbose_name='Durasi Keluhan')),
                ('perjalanan_keluhan', models.TextField(max_length=500, verbose_name='Perjalanan Keluhan')),
                ('aktivitas_fisik', models.CharField(max_length=100, verbose_name='Aktivitas Fisik')),
                ('pemeriksaan_penunjang', models.FileField(blank=True, max_length=250, upload_to='', verbose_name='Pemeriksaan Penunjang')),
                ('tanggal_terapi', models.DateField(default=django.utils.timezone.now, help_text='TTTT-BB-HH', verbose_name='Tanggal')),
                ('slot_waktu', models.IntegerField(choices=[('09:00', '09:00'), ('10:00', '10:00'), ('11:00', '11:00'), ('13:00', '13:00'), ('14:00', '14:00'), ('15:00', '15:00')], default=6)),
                ('kunjungan_ke', models.IntegerField(default=0, verbose_name='Kunjungan ke')),
                ('waktu_mulai', models.TimeField(verbose_name='Waktu Mulai')),
                ('waktu_selesai', models.TimeField(verbose_name='Waktu Selesai')),
                ('status', models.CharField(choices=[('Menunggu Konfirmasi', 'Menunggu Konfirmasi'), ('Dikonfirmasi', 'Dikonfirmasi'), ('Menunggu Pembatalan', 'Menunggu Pembatalan'), ('Dibatalkan', 'Dibatalkan'), ('Sedang Berlangsung', 'Sedang Berlangsung'), ('Tidak Hadir', 'Tidak Hadir'), ('Menunggu Pembayaran', 'Menunggu Pembayaran'), ('Selesai', 'Selesai')], max_length=30, verbose_name='Status')),
                ('catatan_terapis', models.CharField(blank=True, default='', max_length=500, verbose_name='Catatan Terapis')),
                ('alasan_batal', models.CharField(blank=True, default='', max_length=250, verbose_name='Alasan Batal')),
                ('nominal_pembayaran', models.CharField(blank=True, default='', max_length=50, verbose_name='Nominal Pembayaran')),
                ('metode_pembayaran', models.CharField(choices=[('Tunai', 'Tunai'), ('Transfer', 'Transfer'), ('QRIS', 'QRIS')], default='', max_length=10, verbose_name='Cara Pembayaran')),
                ('pasien', models.ForeignKey(default=0, on_delete=django.db.models.deletion.RESTRICT, to='account.pasien')),
                ('terapis', models.ForeignKey(default=0, on_delete=django.db.models.deletion.RESTRICT, to='account.terapis')),
            ],
            options={
                'db_table': 'Appointment',
            },
        ),
        migrations.CreateModel(
            name='AppointmentStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('0', 'Menunggu Konfirmasi'), ('1', 'Dikonfirmasi'), ('2', 'Menunggu Pembatalan'), ('3', 'Dibatalkan'), ('4', 'Sedang Berlangsung'), ('5', 'Tidak Hadir'), ('6', 'Menunggu Pembayaran'), ('7', 'Selesai')], default='0', max_length=25)),
                ('appointment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='appointment_status', to='daftar_terapi.appointment')),
            ],
        ),
    ]