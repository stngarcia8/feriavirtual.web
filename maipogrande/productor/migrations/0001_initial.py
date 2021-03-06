# Generated by Django 3.1.1 on 2020-10-06 23:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ProductID', models.CharField(blank=True, max_length=40)),
                ('ClientID', models.CharField(blank=True, max_length=40)),
                ('ProductName', models.CharField(max_length=50, verbose_name='Nombre producto')),
                ('Observation', models.CharField(max_length=100, verbose_name='Observación')),
                ('ProductValue', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Valor del producto')),
                ('ProductQuantity', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Cantidad de productos (medido en KG)')),
                ('User', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('id',),
            },
        ),
    ]
