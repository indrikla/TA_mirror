# Generated by Django 4.1.6 on 2023-04-24 18:35

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_alter_pasien_tanggal_lahir'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pasien',
            name='tanggal_lahir',
            field=models.DateField(validators=[django.core.validators.MaxValueValidator(datetime.date.today), django.core.validators.MinValueValidator(datetime.date(1923, 4, 25))]),
        ),
    ]
