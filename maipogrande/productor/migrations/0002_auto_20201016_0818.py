# Generated by Django 3.1.1 on 2020-10-16 11:18

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('productor', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='ProductID',
            field=models.CharField(default=uuid.UUID('07b3b003-19e0-40a1-a800-90ba0b602636'), max_length=40),
        ),
    ]
