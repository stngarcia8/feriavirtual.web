# Generated by Django 3.1.1 on 2020-10-20 12:28

import datetime
import django.core.validators
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('cexterno', '0006_auto_20201019_2241'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='exportproduct',
            options={'ordering': ('ProductName',)},
        ),
        migrations.AlterField(
            model_name='order',
            name='OrderDate',
            field=models.DateField(default=datetime.date.today, help_text='Formato: dd/mm/aaaa', verbose_name='Fecha orden de compra'),
        ),
        migrations.AlterField(
            model_name='order',
            name='OrderDiscount',
            field=models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)], verbose_name='¿Tiene descuento?'),
        ),
        migrations.AlterField(
            model_name='orderdetail',
            name='OrderDetailID',
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        ),
        migrations.AlterField(
            model_name='orderdetail',
            name='Quantity',
            field=models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(99999)], verbose_name='Cantidad de productos (medido en KG)'),
        ),
    ]
