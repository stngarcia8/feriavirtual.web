# Generated by Django 3.1.1 on 2020-10-08 02:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('transportista', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('VehicleID', models.CharField(max_length=40)),
                ('ClientID', models.CharField(max_length=40)),
                ('VehiclePatent', models.CharField(max_length=10, verbose_name='Patente de vehículo')),
                ('VehicleModel', models.CharField(max_length=100, verbose_name='Tipo vehículo')),
                ('VehicleCapacity', models.DecimalField(decimal_places=2, help_text='(ej: 5200,5)', max_digits=9, verbose_name='Capacidad de carga en Kg')),
                ('VehicleAvailable', models.BooleanField(help_text='(ej: Si)', verbose_name='Vehículo disponible')),
                ('User', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('VehicleType', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='transportista.vehicletype', verbose_name='Seleccione tipo de transporte')),
            ],
        ),
        migrations.DeleteModel(
            name='TransportInfo',
        ),
    ]
