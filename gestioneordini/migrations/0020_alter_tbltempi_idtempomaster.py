# Generated by Django 3.2.3 on 2022-10-24 18:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestioneordini', '0019_auto_20221005_1554'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tbltempi',
            name='idtempomaster',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='gestioneordini.tbltempimaster'),
        ),
    ]
