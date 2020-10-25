# Generated by Django 3.1.1 on 2020-10-23 23:43

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ExportProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ProductName', models.CharField(max_length=50, verbose_name='Producto')),
                ('User', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('ProductName',),
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('OrderID', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('ClientID', models.CharField(blank=True, max_length=40, null=True)),
                ('OrderDate', models.DateField(default=datetime.date.today, help_text='Formato: dd/mm/aaaa', verbose_name='Fecha orden de compra')),
                ('OrderDiscount', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)], verbose_name='¿Tiene descuento?')),
                ('Observation', models.CharField(blank=True, max_length=100, null=True, verbose_name='Observación')),
            ],
            options={
                'verbose_name': 'Orden de compra',
                'verbose_name_plural': 'Ordenes de compras',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='PaymentCondition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ConditionID', models.IntegerField(default=1)),
                ('ConditionDescription', models.CharField(max_length=25, verbose_name='Condición de pago')),
            ],
            options={
                'ordering': ('ConditionID',),
            },
        ),
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('OrderDetailID', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('Quantity', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(99999)], verbose_name='Cantidad de productos (medido en KG)')),
                ('Order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cexterno.order')),
                ('Product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cexterno.exportproduct', verbose_name='Seleccione producto')),
            ],
            options={
                'verbose_name': 'Detalle de orden',
                'verbose_name_plural': 'Detalles de ordenes',
                'ordering': ('id',),
            },
        ),
        migrations.AddField(
            model_name='order',
            name='PaymentCondition',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cexterno.paymentcondition', verbose_name='Condiciones de pago'),
        ),
        migrations.AddField(
            model_name='order',
            name='User',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
