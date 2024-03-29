# Generated by Django 3.2.3 on 2022-10-04 12:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestioneordini', '0006_alter_tbltempi_idoperatore'),
    ]

    operations = [
        migrations.CreateModel(
            name='tblTempiMaster',
            fields=[
                ('idtempomaster', models.AutoField(primary_key=True, serialize=False)),
                ('datatempo', models.DateField(blank=True, null=True, verbose_name='Data')),
                ('quantity', models.FloatField(blank=True, null=True, verbose_name='Quantità Presa Tempo')),
                ('id_linea', models.ForeignKey(blank=True, db_column='id_linea', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='gestioneordini.tbllineelav')),
                ('iddettordine', models.ForeignKey(blank=True, db_column='iddettordine', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='gestioneordini.tbldettaglioordini')),
            ],
        ),
        migrations.AddField(
            model_name='tbltempi',
            name='idtempomaster',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='gestioneordini.tbltempimaster'),
        ),
    ]
