# Generated by Django 3.1.1 on 2020-10-30 02:29

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
            name='LoginSession',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('UserId', models.CharField(max_length=150)),
                ('ClientID', models.CharField(max_length=150)),
                ('Username', models.CharField(max_length=150)),
                ('FullName', models.CharField(max_length=250)),
                ('Email', models.CharField(max_length=254)),
                ('ProfileID', models.PositiveIntegerField(default=0, verbose_name='id perfil')),
                ('ProfileName', models.CharField(max_length=50)),
                ('User', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
