# Generated by Django 3.2.3 on 2023-01-05 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestioneordini', '0020_alter_tbltempi_idtempomaster'),
    ]

    operations = [
        migrations.AddField(
            model_name='tblclienti',
            name='visualizza_come',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
