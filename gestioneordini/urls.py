from django.urls import path
from . import views
from .views import OpenTimeView, dashboard

app_name="gestioneordini"

urlpatterns = [
    path('', 
        dashboard,
        name='homeview'),  
    
    path('lista_ordini/', 
        views.ListaOrdiniView.as_view(), 
        name="lista_ordini"),
    
    path('dettaglio/<int:pk>/<int:id_linea>/<int:idtempomaster>/',
        views.visualizza_dettaglio, 
        name="visualizza_dettaglio"),
    
    path('dettaglio_da_linea/<int:pk>/<int:id_linea>/<int:idtempomaster>/', 
        views.mostra_operatori_linea, 
        name="visualizza_dettaglio_da_linea"),
    
    path('cerca/',
        views.cerca, 
        name="funzione_cerca"),

    path('dashboard/', 
        views.dashboard, 
        name="dashboard"),
    
    path('prova/', 
        views.OperatorView.as_view(),
        name="visualizza_operatori"),    
    
    path(
        "dettaglio/<int:pk>/<int:pk_linea>/<int:idtempomaster>/crea_tempo/",
        views.aggiungi_operatore_attivo,
        name="crea_tempo",
    ),
    
    path(
        "dettaglio/<int:pk>/<int:pk_linea>/<int:idtempomaster>/crea_tempo_barcode/",
        views.cerca_operatore,
        name="crea_tempo_barcode",
    ),

    path(
        'tempi_aperti/', 
        OpenTimeView.as_view(),
        name="tempi_aperti"        
    ),
    
    path(
        "dettaglio/elimina-operatore/<int:idtempo>/",
        views.delete_operatore,
        name="cancella_operatore",
    ),
    
    path(
        "dettaglio/<int:pk>/",
        views.cerca_operatore,
        name="cerca_operatore_attivo",
    ),
    
    path(
        "vedi-linea/<int:pk>/",
        views.mostra_operatori_linea,        
        name="vedi-linea",        
    ),
    
    path("chiudi-operatore/<int:idtempo>/",
        views.chiudi_operatore,
        name="chiudi_operatore"),
    
    path("dettaglio/<int:pk>/aggiorna-operatore/<int:iddett>/",
        views.aggiorna_operatore_attivo,
        name="aggiorna_operatore"),
    
    path("chiudi-lavorazione/<int:pk>/<int:id_linea>/",
        views.chiudi_lavorazione,
        name="chiudi_lavorazione"),
    
    path("apri-lavorazione/<int:pk>/<int:id_linea>/",
        views.apri_lavorazione,
        name="apri_lavorazione"),
    
    path("cancella-lavorazione/<int:pk>/",
        views.delete_tempo_master,
        name="cancella_lavorazione"),
    
    path("update-quantity/<int:pk>/",
        views.update_quantity_tempo_master,
        name="update_quantity"),
    
    path("update-line-note/<int:pk>/",
        views.update_line_note_tempo_master,
        name="update_note"),
    
    path(
        "add-to-line/<int:id_linea>/",
        views.add_line_search_order,        
        name="add-to-line",        
    ),
    
    path(
        "add-master/<int:pk>/<int:id_linea>/",
        views.add_master_time,
        name="add-master"
    ),
    
    path(
        "add-master-barcode/<int:id_linea>/",
        views.add_master_time_barcode,
        name="add-master-barcode"
    ),    
    
    path(
        "ask-for-close/<int:idtempo>/<int:iddettaglio>/<int:pk_linea>/<int:idtempomaster>/",
        views.ask_for_close_operator,
        name="ask-for-close"
    ),
    
    path(
        "add-operator-auto/<int:pk>/<int:id_operatore>/<int:id_linea>/<int:id_tempomaster>/<str:starttime>/",
        views.aggiungi_operatore_auto,
        name="add-auto"
    ),
    
    path(
        "view-single-line/<int:id_linea>/",
        views.view_single_line_open_times,
        name="single-line"
    ),
    
    # 04/10/2023 - Eliminata perchè è compresa nella precedente
    # path(
    #     "view-all-tracked/",
    #     views.view_all_tracked,
    #     name="view-all-tracked"
    # ),
    
    
]
