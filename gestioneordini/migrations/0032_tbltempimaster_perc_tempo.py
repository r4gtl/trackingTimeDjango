# Generated by Django 3.2.3 on 2024-07-06 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestioneordini', '0031_auto_20240706_1426'),
    ]

    operations = [
        migrations.AddField(
            model_name='tbltempimaster',
            name='perc_tempo',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]
