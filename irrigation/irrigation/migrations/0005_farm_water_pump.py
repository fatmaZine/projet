# Generated by Django 4.2.1 on 2023-06-22 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('irrigation', '0004_capteurtemperature_capteurhumidite'),
    ]

    operations = [
        migrations.AddField(
            model_name='farm',
            name='water_pump',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=2),
        ),
    ]
