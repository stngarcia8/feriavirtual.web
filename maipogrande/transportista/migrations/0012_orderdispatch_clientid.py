# Generated by Django 3.1.1 on 2020-11-06 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transportista', '0011_auto_20201106_0053'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdispatch',
            name='ClientID',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
    ]
