# Generated by Django 3.1.1 on 2020-10-09 03:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transportista', '0004_auto_20201008_1956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicletype',
            name='VehicleTypeDescription',
            field=models.CharField(max_length=100, verbose_name='Tipo transporte'),
        ),
    ]
