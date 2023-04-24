# Generated by Django 4.1.6 on 2023-04-21 09:45

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('daftar_terapi', '0003_alter_appointment_slot_waktu'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='status',
            field=models.CharField(choices=[(0, 'Menunggu Konfirmasi'), (1, 'Dikonfirmasi'), (2, 'Sedang Berlangsung'), (3, 'Menunggu Pembayaran'), (4, 'Selesai'), (5, 'Menunggu Pembatalan'), (6, 'Dibatalkan'), (7, 'Tidak Hadir')], max_length=30, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='tanggal_terapi',
            field=models.DateField(default=django.utils.timezone.now, help_text='TTTT-BB-HH', verbose_name='Tanggal Terapi'),
        ),
    ]