# Generated by Django 3.2.3 on 2023-07-06 18:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gestioneordini', '0025_auto_20230705_2017'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tblcomponenti',
            name='tempolavorazione',
        ),
    ]
