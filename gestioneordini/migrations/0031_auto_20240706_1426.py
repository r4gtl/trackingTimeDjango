# Generated by Django 3.2.3 on 2024-07-06 12:26

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestioneordini', '0030_tbldestinazioni'),
    ]

    operations = [
        migrations.AddField(
            model_name='tbltempimaster',
            name='data_chiusura_tempo',
            field=models.DateField(blank=True, null=True, verbose_name='Data Chiusura'),
        ),
        migrations.AddField(
            model_name='tbltempimaster',
            name='minuti_medi_lavorazione',
            field=models.IntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(60)]),
        ),
        migrations.AddField(
            model_name='tbltempimaster',
            name='ore_medie_lavorazione',
            field=models.IntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(99)]),
        ),
        migrations.AddField(
            model_name='tbltempimaster',
            name='secondi_medi_lavorazione',
            field=models.IntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(60)]),
        ),
    ]
