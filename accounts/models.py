# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Qryoperatoriattivi(models.Model):
    id_operatore = models.IntegerField(blank=True, null=True)
    cognome = models.CharField(max_length=255, blank=True, null=True)
    nome = models.CharField(max_length=255, blank=True, null=True)
    idfase = models.IntegerField(blank=True, null=True)
    nordine = models.CharField(max_length=50, blank=True, null=True)
    dataordine = models.DateTimeField(blank=True, null=True)
    idcliente = models.IntegerField(blank=True, null=True)
    iddettordine = models.IntegerField(blank=True, null=True)
    ncommessa = models.CharField(max_length=50, blank=True, null=True)
    quantità = models.FloatField(blank=True, null=True)
    orafine = models.DateTimeField(blank=True, null=True)
    idcollegamento = models.IntegerField(blank=True, null=True)
    idcomponente = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'qryoperatoriattivi'
