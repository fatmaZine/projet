# Generated by Django 4.2.1 on 2023-06-21 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('irrigation', '0002_zone_nom_plante'),
    ]

    operations = [
        migrations.AddField(
            model_name='plant',
            name='nbre_valve',
            field=models.IntegerField(default='2'),
        ),
    ]
