# Generated by Django 3.2.3 on 2022-10-04 13:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestioneordini', '0013_rename_id_dettordine_tbltempimaster_iddettordine'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tbltempi',
            name='idtempomaster',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='gestioneordini.tbltempimaster'),
        ),
    ]
