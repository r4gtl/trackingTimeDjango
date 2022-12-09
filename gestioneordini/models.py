# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = True` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from enum import unique
from django.db import models
from django.urls import reverse
from django.db.models import Max
import datetime


class TRicerca(models.Model):
    id = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=50, blank=True, null=True)
    chiave = models.CharField(max_length=50, blank=True, null=True)
    tipochiavetesto = models.BooleanField(blank=True, null=True)
    strsql = models.CharField(max_length=10485760, blank=True, null=True)
    ordinamento = models.CharField(max_length=50, blank=True, null=True)
    ordinamento2 = models.CharField(max_length=50, blank=True, null=True)
    campi = models.CharField(max_length=50, blank=True, null=True)
    colonne = models.IntegerField(blank=True, null=True)
    predefinito = models.CharField(max_length=50, blank=True, null=True)
    originecombo = models.CharField(max_length=50, blank=True, null=True)
    dacompilare = models.CharField(max_length=255, blank=True, null=True)
    vaiarecord = models.BooleanField(blank=True, null=True)
    formriferimento = models.CharField(max_length=50, blank=True, null=True)
    mionome = models.CharField(max_length=50, blank=True, null=True)
    focus = models.CharField(max_length=255, blank=True, null=True)
    larghezza = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nome


    class Meta:
        managed = True
        db_table = 't_ricerca'
        verbose_name = "t_ricerca"
        verbose_name_plural = "t_ricerca"

    
    


class Tblazienda(models.Model):
    idragsoc = models.IntegerField(primary_key=True)
    ragionesociale = models.CharField(max_length=50, blank=True, null=True)
    indirizzo = models.CharField(max_length=50, blank=True, null=True)
    cap = models.CharField(max_length=50, blank=True, null=True)
    comune = models.CharField(max_length=50, blank=True, null=True)
    provincia = models.CharField(max_length=50, blank=True, null=True)
    partitaiva = models.CharField(max_length=50, blank=True, null=True)
    ufficio = models.CharField(max_length=50, blank=True, null=True)
    codeori = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tblazienda'
        verbose_name = "tblazienda"
        verbose_name_plural = "tblazienda"


class Tblcave(models.Model):
    idcave = models.IntegerField(primary_key=True)
    cave = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tblcave'
        verbose_name = "tblcave"
        verbose_name_plural = "tblcave"


class Tblclienti(models.Model):
    idcliente = models.IntegerField(primary_key=True)
    ragionesociale = models.CharField(max_length=100, blank=True, null=True)
    indirizzo = models.CharField(max_length=100, blank=True, null=True)
    cap = models.CharField(max_length=50, blank=True, null=True)
    città = models.CharField(max_length=50, blank=True, null=True)
    provincia = models.CharField(max_length=50, blank=True, null=True)
    piva = models.CharField(max_length=50, blank=True, null=True)
    tel = models.CharField(max_length=50, blank=True, null=True)
    fax = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    cf = models.CharField(max_length=255, blank=True, null=True)
    ufficioiva = models.CharField(max_length=255, blank=True, null=True)
    idpagamento = models.IntegerField(blank=True, null=True)
    idiva = models.IntegerField(blank=True, null=True)
    idbanca = models.IntegerField(blank=True, null=True)
    agenzia = models.CharField(max_length=255, blank=True, null=True)
    iban = models.CharField(max_length=255, blank=True, null=True)
    nascondi = models.BooleanField(blank=True, null=True)
    pec = models.CharField(max_length=255, blank=True, null=True)
    codicedestinatario = models.CharField(max_length=255, blank=True, null=True)
    codeori = models.CharField(max_length=255, blank=True, null=True)
    idnazione = models.IntegerField(blank=True, null=True)
    dichintento = models.CharField(max_length=255, blank=True, null=True)
    prezzoordine = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tblclienti'
        verbose_name = "tblclienti"
        verbose_name_plural = "tblclienti"
    
    def __str__(self):
        return self.ragionesociale


class Tblcollegamenti(models.Model):
    idcollegamento = models.IntegerField(primary_key=True)
    codicecollegamento = models.CharField(max_length=50, blank=True, null=True)
    descrizione = models.CharField(max_length=50, blank=True, null=True)
    idcliente = models.IntegerField(blank=True, null=True)
    tempolavorazione = models.FloatField(blank=True, null=True)
    idcausale = models.IntegerField(blank=True, null=True)
    prezzo = models.FloatField(blank=True, null=True)
    iddestinazione = models.IntegerField(blank=True, null=True)
    idgruppo = models.IntegerField(blank=True, null=True)
    costo = models.FloatField(blank=True, null=True)
    grcavicliente = models.BooleanField(blank=True, null=True)
    schedatecnica = models.CharField(max_length=10485760, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tblcollegamenti'
        verbose_name = "tblcollegamenti"
        verbose_name_plural = "tblcollegamenti"

    def __str__(self):
        return self.codicecollegamento



class Tblcomponenti(models.Model):
    idcomponente = models.IntegerField(primary_key=True)
    idtipocomponente = models.IntegerField(blank=True, null=True)
    idcliente = models.IntegerField(blank=True, null=True)
    codice = models.CharField(max_length=255, blank=True, null=True)
    descrizione = models.CharField(max_length=255, blank=True, null=True)
    poli1 = models.CharField(max_length=255, blank=True, null=True)
    schedatecnica = models.CharField(max_length=10485760, blank=True, null=True)
    tempolavorazione = models.FloatField(blank=True, null=True)
    iddestinazione = models.IntegerField(blank=True, null=True)
    idgruppo = models.IntegerField(blank=True, null=True)
    idmec = models.IntegerField(blank=True, null=True)
    idcausale = models.IntegerField(blank=True, null=True)
    prezzo = models.FloatField(blank=True, null=True)
    idpoli = models.IntegerField(blank=True, null=True)
    idcave = models.IntegerField(blank=True, null=True)
    costo = models.FloatField(blank=True, null=True)
    lr = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tblcomponenti'
        verbose_name = "tblcomponenti"
        verbose_name_plural = "tblcomponenti"

    def __str__(self):
        return self.codice



class Tbldettaglioordini(models.Model):
    iddettordine = models.IntegerField(primary_key=True, unique=True)
    idordine = models.ForeignKey('Tblordini', models.DO_NOTHING, db_column='idordine', blank=True, null= True)
    idcollegamento = models.ForeignKey('TblCollegamenti', models.DO_NOTHING, db_column='idcollegamento',  blank=True, null= True)
    posizione = models.FloatField(blank=True, null=True)
    idcomponente = models.ForeignKey('TblComponenti',models.DO_NOTHING, db_column='idcomponente',  blank=True, null= True)
    ncommessa = models.CharField(max_length=50, blank=True, null=True)
    quantità = models.FloatField(blank=True, null=True)
    prezzo = models.FloatField(blank=True, null=True)
    dataconsegna = models.DateField(blank=True, null=True)
    note = models.CharField(max_length=10485760, blank=True, null=True)
    iddestinazione = models.IntegerField(blank=True, null=True)
    idcausale = models.IntegerField(blank=True, null=True)
    descrizione = models.CharField(max_length=255, blank=True, null=True)
    ingaranzia = models.BooleanField(blank=True, null=True)
    completato = models.BooleanField(blank=True, null=True)
    inlavoro = models.BooleanField(blank=True, null=True)
    quantitatempo = models.FloatField(blank=True, null=True)
    noteconteggi = models.CharField(max_length=10485760, blank=True, null=True)
    grcavicliente = models.BooleanField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse("visualizza_dettaglio", kwargs={"pk": self.pk})

    class Meta:
        managed = True
        db_table = 'tbldettaglioordini'
        verbose_name = "tbldettaglioordini"
        verbose_name_plural = "tbldettaglioordini"


class Tbldettcollegamenti(models.Model):
    iddettcollegamento = models.IntegerField(primary_key=True)
    idcollegamento = models.ForeignKey(Tblcollegamenti, models.DO_NOTHING, db_column='idcollegamento', blank=True, null=True)
    idcomponente = models.IntegerField(blank=True, null=True)
    quantità = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tbldettcollegamenti'
        verbose_name = "tbldettcollegamenti"
        verbose_name_plural = "tbldettcollegamenti"


class Tblfasi(models.Model):
    idfase = models.IntegerField(primary_key=True)
    fase = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tblfasi'
        verbose_name = "tblfasi"
        verbose_name_plural = "tblfasi"

    def __str__(self):
        return self.fase


class Tblgruppi(models.Model):
    idgruppo = models.IntegerField(primary_key=True)
    idmec = models.IntegerField()
    idpoli = models.IntegerField()
    idcave = models.IntegerField()
    idtipocollegamento = models.IntegerField(blank=True, null=True)
    idqseparatori = models.IntegerField(blank=True, null=True)
    idpassocava = models.IntegerField(blank=True, null=True)
    descrizione = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tblgruppi'
        verbose_name = "tblgruppi"
        verbose_name_plural = "tblgruppi"


class Tblmec(models.Model):
    idmec = models.IntegerField(primary_key=True)
    mec = models.CharField(max_length=50, blank=True, null=True)
    note = models.CharField(max_length=10485760, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tblmec'
        verbose_name = "tblmec"
        verbose_name_plural = "tblmec"


class Tbloperatori(models.Model):
    idoperatore = models.IntegerField(primary_key=True)
    cognome = models.CharField(max_length=255, blank=True, null=True)
    nome = models.CharField(max_length=255, blank=True, null=True)
    dimesso=models.BooleanField(default=False, null=False, blank=False)

    class Meta:
        managed = False
        db_table = 'tbloperatori'
        verbose_name = "tbloperatori"
        verbose_name_plural = "tbloperatori"

    def __str__(self):        
        return str(self.cognome) + " " + str(self.nome)
    
    
class Tblordini(models.Model):
    idordine = models.IntegerField(primary_key=True)
    nordine = models.CharField(max_length=50, blank=True, null=True)
    dataordine = models.DateTimeField(db_column='dataordine', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'.    
    idcliente = models.ForeignKey('Tblclienti', models.DO_NOTHING, db_column='idcliente', blank=True, null= True)

    class Meta:
        managed = True
        db_table = 'tblordini'
        verbose_name = "tblordini"
        verbose_name_plural = "tblordini"

    def __str__(self):
        return self.nordine

class Tblpoli(models.Model):
    idpoli = models.IntegerField(primary_key=True)
    poli = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tblpoli'
        verbose_name = "tblpoli"
        verbose_name_plural = "tblpoli"


class TblLineeLav(models.Model):
    id_linea = models.AutoField(primary_key=True)
    descrizione_linea = models.CharField(max_length=50, blank=False, null=False)

    class Meta:
        managed = False
        db_table = "tbl_linee_lav"
    
    '''Recupero l'ordine in lavorazione'''
    # Modifica effettuata in data 04/10/2022 perchè serve prendere più tempi per un singolo dettaglio
    # def get_line(self):
    #     tempi_object = Tbltempi.objects.filter(orafine__isnull = True).order_by('-orainizio')                       
    #     partial_qs=tempi_object.values('id_linea').annotate(ultimo=Max('orainizio'))        
    #     tempi_object=tempi_object.filter(orainizio__in=partial_qs.values('ultimo').order_by('-orainizio')).filter(id_linea=self.id_linea).first()
    #     #print("tempi_object: " + str(tempi_object))
    #     return tempi_object 
    def get_line(self):
        tempi_object = tblTempiMaster.objects.filter(completato=False).order_by('-datatempo')                       
        partial_qs=tempi_object.values('id_linea').annotate(ultimo=Max('datatempo'))        
        tempi_object=tempi_object.filter(datatempo__in=partial_qs.values('ultimo').order_by('-datatempo')).filter(id_linea=self.id_linea).first()
        
        return tempi_object 

    def __str__(self):
        return self.descrizione_linea

class tblTempiMaster(models.Model):
    idtempomaster = models.AutoField(primary_key=True)
    iddettordine = models.ForeignKey(Tbldettaglioordini, on_delete=models.DO_NOTHING, to_field='iddettordine', db_column='iddettordine', blank=True, null=True)
    datatempo = models.DateField(blank=True, null=True, verbose_name="Data")  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'.
    quantity = models.FloatField(blank=True, null=True, verbose_name="Quantità Presa Tempo")
    id_linea = models.ForeignKey(TblLineeLav, on_delete=models.DO_NOTHING, db_column='id_linea',blank=True, null=True)
    completato = models.BooleanField(blank=True, null=True, default=False)
    inlavoro = models.BooleanField(blank=True, null=True, default=True)
    
    class Meta:
        managed = True
        db_table = 'tbltempimaster'
        verbose_name = "tbltempimaster"
        verbose_name_plural = "tbltempimaster"

class Tbltempi(models.Model):
    idtempo = models.AutoField(primary_key=True)
    iddettordine = models.ForeignKey(Tbldettaglioordini, on_delete=models.DO_NOTHING, to_field='iddettordine', db_column='iddettordine', blank=True, null=True)
    idoperatore = models.ForeignKey(Tbloperatori, on_delete=models.DO_NOTHING, db_column='idoperatore', blank=False, null=False)
    idfase = models.ForeignKey(Tblfasi, on_delete=models.DO_NOTHING, db_column='idfase', blank=True, null=True)
    datatempo = models.DateField(blank=True, null=True, verbose_name="Data")  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'.
    orainizio = models.TimeField(blank=True, null=True, verbose_name="Ora Inizio")
    orafine = models.TimeField(blank=True, null=True, verbose_name="Ora Fine")
    note = models.CharField(max_length=10485760, blank=True, null=True, verbose_name="Note")
    quantitatemporiparazione = models.FloatField(blank=True, null=True, verbose_name="Quantità Riparati")
    id_linea = models.ForeignKey(TblLineeLav, on_delete=models.DO_NOTHING, db_column='id_linea', blank=True, null=True)
    idtempomaster =  models.ForeignKey(tblTempiMaster, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tbltempi'
        verbose_name = "tbltempi"
        verbose_name_plural = "tbltempi"
        
        constraints = [
        models.CheckConstraint(
            check=models.Q(orainizio__lte=datetime.time(6, 00, 00)),
            name='created_at_cannot_be_past_date'
        )
        ]
        
    
    def get_absolute_url(self):
        return reverse("visualizza_dettaglio", kwargs={"pk": self.idtempo})


class Tbltipocomponenti(models.Model):
    idtipocomponente = models.IntegerField(primary_key=True)
    tipocomponente = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tbltipocomponenti'
        verbose_name = "tbltipocomponenti"
        verbose_name_plural = "tbltipocomponenti"


class Tblxrmecclienti(models.Model):
    idxrmecclienti = models.IntegerField(primary_key=True)
    idcliente = models.IntegerField(blank=True, null=True)
    idmec = models.IntegerField(blank=True, null=True)
    costo = models.FloatField(blank=True, null=True)
    idgruppo = models.IntegerField(blank=True, null=True)
    idpoli = models.IntegerField(blank=True, null=True)
    idcave = models.IntegerField(blank=True, null=True)
    idtipocollegamento = models.IntegerField(blank=True, null=True)
    idqseparatori = models.IntegerField(blank=True, null=True)
    idpassocava = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tblxrmecclienti'
        verbose_name = "tblxrmecclienti"
        verbose_name_plural = "tblxrmecclienti"

class Qryordiniiniziale(models.Model):
    id_dett_ord = models.AutoField(primary_key=True)
    idordine = models.IntegerField(blank=True, null=True)
    nordine = models.CharField(max_length=50, blank=True, null=True)
    dataordine = models.DateTimeField(blank=True, null=True)
    ncommessa = models.CharField(max_length=50, blank=True, null=True)
    ragionesociale = models.CharField(max_length=100, blank=True, null=True)
    completato = models.BooleanField(blank=True, null=True)
    inlavoro = models.BooleanField(blank=True, null=True)
    idcliente = models.IntegerField(blank=True, null=True)
    idcomponente = models.IntegerField(blank=True, null=True)
    idcollegamento = models.IntegerField(blank=True, null=True)
    codice = models.CharField(max_length=255, blank=True, null=True)
    iddettordine = models.IntegerField(blank=True, null=True)
    codicecollegamento = models.CharField(max_length=50, blank=True, null=True)

    def get_absolute_url(self):
        return reverse("visualizza_dettaglio", kwargs={"pk": self.iddettordine})

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'qryordiniiniziale'
        ordering = ['-dataordine']



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
    codice = models.CharField(max_length=255, blank=True, null=True)
    codicecollegamento = models.CharField(max_length=50, blank=True, null=True)
    fase = models.CharField(max_length=255, blank=True, null=True)
    ragionesociale = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'qryoperatoriattivi'
        ordering = ['-dataordine']

    

