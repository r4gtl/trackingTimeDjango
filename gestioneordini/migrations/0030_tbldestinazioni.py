# Generated by Django 3.2.3 on 2023-09-09 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestioneordini', '0029_auto_20230708_2028'),
    ]

    operations = [
        migrations.CreateModel(
            name='tblDestinazioni',
            fields=[
                ('iddestinazione', models.IntegerField(primary_key=True, serialize=False)),
                ('destinazione', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'verbose_name': 'tbldestinazioni',
                'verbose_name_plural': 'tbldestinazioni',
                'db_table': 'tbldestinazioni',
                'managed': False,
            },
        ),
    ]