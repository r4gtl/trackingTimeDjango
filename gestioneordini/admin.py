from django.contrib import admin
from .models import (
    TRicerca, Tblazienda, Tblcave, 
    Tblclienti,Tblcollegamenti, Tblcomponenti, 
    Tbldettaglioordini,Tbldettcollegamenti, Tblfasi, 
    Tblgruppi, Tblmec, Tbloperatori,
    Tblordini, Tblpoli, Tbltempi, 
    Tbltipocomponenti, Tblxrmecclienti, tblTempiMaster
)

# Register your models here.

class tblTempiMasterModelAdmin(admin.ModelAdmin):
    model = tblTempiMaster
    list_display = ["idtempomaster", "iddettordine", "datatempo",
                    'quantity', 'id_linea',
                    'completato', 'inlavoro'
                    ]
    search_fields = ["datatempo", "idtempomaster"]

class TblTempiModelAdmin(admin.ModelAdmin):
    model = Tbltempi
    list_display = ['idtempo', 'idtempomaster', 'iddettordine', 'idoperatore', 'datatempo', 'orainizio', 'orafine']
    search_fields = ['idtempomaster__idtempomaster'] # Utilizza la doppia underscore notation per la ricerca su ForeignKey
    ordering = ['-datatempo']
    
class TbldettaglioordiniModelAdmin(admin.ModelAdmin):
    model = Tbldettaglioordini
    list_display = ['iddettordine', 'idordine', 'idcollegamento',
                    'posizione', 'idcomponente', 'ncommessa', 'quantità',
                    'dataconsegna'
                    ]
    search_fields = ['ncommessa', 'quantità']
    ordering = ['iddettordine']
    
    

admin.site.register(TRicerca)
admin.site.register(Tblazienda)
admin.site.register(Tblcave)
admin.site.register(Tblclienti)
admin.site.register(Tblcollegamenti)
admin.site.register(Tblcomponenti)
admin.site.register(Tbldettaglioordini, TbldettaglioordiniModelAdmin)
admin.site.register(Tbldettcollegamenti)
admin.site.register(Tblfasi)
admin.site.register(Tblgruppi)
admin.site.register(Tblmec)
admin.site.register(Tbloperatori)
admin.site.register(Tblordini)
admin.site.register(Tblpoli)
admin.site.register(Tbltempi, TblTempiModelAdmin)
admin.site.register(Tbltipocomponenti)
admin.site.register(Tblxrmecclienti)
admin.site.register(tblTempiMaster, tblTempiMasterModelAdmin)
