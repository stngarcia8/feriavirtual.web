# Generated by Django 3.1.1 on 2020-10-24 20:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contratos', '0004_auto_20201024_1713'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='EndDate',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='contract',
            name='StartDate',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
