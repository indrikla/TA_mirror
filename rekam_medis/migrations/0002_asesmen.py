# Generated by Django 4.1.6 on 2023-04-24 18:35

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_alter_pasien_tanggal_lahir'),
        ('rekam_medis', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Asesmen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tanggal_dibuat', models.DateField(default=django.utils.timezone.now, help_text='TTTT-BB-HH', verbose_name='Tanggal Dibuat')),
                ('tipe', models.CharField(choices=[('Fisioterapi', 'Fisioterapi'), ('Terapi Okupasi', 'Terapi Okupasi'), ('Terapi Wicara', 'Terapi Wicara')], max_length=50, null=True, verbose_name='Tipe')),
                ('lampiran', models.FileField(blank=True, max_length=250, upload_to='', verbose_name='Lampiran')),
                ('pasien', models.ForeignKey(default=0, on_delete=django.db.models.deletion.RESTRICT, to='account.pasien')),
                ('terapis', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='terapis_asesmen', to='account.terapis')),
            ],
            options={
                'db_table': 'Asesmen',
            },
        ),
    ]
