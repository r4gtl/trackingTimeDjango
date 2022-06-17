from .models import Tbldettaglioordini
from django.urls import path
from . import views
from .views import dashboard, home


urlpatterns = [
    path('lista_ordini/', views.ListaOrdiniView.as_view(), name="lista_ordini"),
    path('dettaglio/<int:pk>/', views.visualizza_dettaglio, name="visualizza_dettaglio"),
    path('cerca/', views.cerca, name="funzione_cerca"),

    path('dashboard/', views.dashboard, name="dashboard"),
    path('prova/', views.OperatorView.as_view(), name="visualizza_operatori"),
    path(
        "dettaglio/<int:pk>/crea_tempo/",
        views.aggiungi_operatore_attivo,
        name="crea_tempo",
    ),
    path(
        "dettaglio/<int:pk>/crea_tempo_barcode/",
        views.cerca_operatore,
        name="crea_tempo_barcode",
    ),

    path('', dashboard, name='homeview'),
    path(
        "dettaglio/<int:id>/elimina-operatore/<int:pk>/",
        views.CancellaOperatore.as_view(),
        name="cancella_operatore",
    ),
    path(
        "dettaglio/<int:pk>/",
        views.cerca_operatore,
        name="cerca_operatore_attivo",
    ),
    path("chiudi-operatore/<int:pk>/", views.chiudi_operatore, name="chiudi_operatore"),
    path("dettaglio/<int:id>/aggiorna-operatore/<int:pk>/", views.TempoUpdateView.as_view(), name="aggiorna_operatore"),
    #path("aggiorna-operatore/<int:pk>/", views.TempoUpdateView.as_view(), name="aggiorna_operatore"),
    path("chiudi-lavorazione/<int:pk>/", views.chiudi_lavorazione, name="chiudi_lavorazione"),
    path("apri-lavorazione/<int:pk>/", views.apri_lavorazione, name="apri_lavorazione"),

    


    ]