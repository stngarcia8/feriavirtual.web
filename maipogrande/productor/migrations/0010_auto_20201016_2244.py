# Generated by Django 3.1.1 on 2020-10-17 01:44

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('productor', '0009_auto_20201016_2146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='ProductID',
            field=models.CharField(default=uuid.UUID('660d23c8-d169-4df3-919e-fe35b164b86e'), max_length=40),
        ),
    ]
