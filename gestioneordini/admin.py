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
    search_fields = ["datatempo"]

class TblTempiModelAdmin(admin.ModelAdmin):
    model = Tbltempi
    list_display = ['idtempo', 'orainizio']
    search_fields = ['orainizio']
    ordering = ['orainizio']
    

admin.site.register(TRicerca)
admin.site.register(Tblazienda)
admin.site.register(Tblcave)
admin.site.register(Tblclienti)
admin.site.register(Tblcollegamenti)
admin.site.register(Tblcomponenti)
admin.site.register(Tbldettaglioordini)
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
