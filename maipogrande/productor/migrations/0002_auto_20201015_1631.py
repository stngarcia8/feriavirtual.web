# Generated by Django 3.1.1 on 2020-10-15 19:31

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
            field=models.CharField(default=uuid.UUID('aa55c712-dae0-4ef1-96b3-a4805f35eb4a'), max_length=40),
        ),
    ]
