# Generated by Django 3.1.1 on 2020-10-19 00:15

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('cexterno', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='OrderID',
            field=models.CharField(default=uuid.UUID('b6950a23-57c4-43b0-bb30-60e773ef478d'), max_length=40),
        ),
        migrations.AlterField(
            model_name='orderdetail',
            name='OrderDetailID',
            field=models.CharField(default=uuid.UUID('d21f5fde-b506-4236-8162-e095b904aecb'), max_length=40),
        ),
    ]