# Generated by Django 3.1.1 on 2020-10-08 15:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transportista', '0002_auto_20201007_2317'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='VehicleType',
            new_name='VehicleTypeDescription',
        ),
    ]
