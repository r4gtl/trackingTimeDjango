from django.forms.forms import Form
from django.forms.models import ModelChoiceField
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login
from django.views.generic.list import ListView
from django.urls import reverse_lazy, reverse
from django.db.models import Count, Q, F, DurationField, ExpressionWrapper, Sum, Max
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django_filters.views import FilterView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .models import TblLineeLav, Tbldettaglioordini, Tblfasi, Tbloperatori, Tbltempi, tblTempiMaster
from .filters import OrderFilter
from .forms import (
        FormDettaglio, TempoModelForm,
        FormMaster, QuantityModelForm,
        AskForCloseModelForm, NoteLineaModelForm,
        FormMediaTempi
)
from datetime import time, timedelta, date , datetime
#import datetime
from django.contrib import messages
from django.utils import timezone
from .utilities import (check_barcode, 
                        check_start_time, 
                        check_end_time, 
                        check_time_range, 
                        get_sec,
                        get_if_media_tempo, get_tempo_medio,
                        get_perc_differenza,
                        get_tempo_nominale,
                        get_tempo_nominale_registrato,
)




'''
In data 04/09/2022 Vanessa dice che devono prendere più tempi per una sola riga di dettaglio.
Questo comporta il dover gestire il tutto con una nuova tabella (tblTempiMaster), in cui
mettiamo in collegamento i tempi e il dettaglio ordini. 

In data 16/11/2022 Vanessa e Paolo dicono che serve inserire una presa tempo nuova prima che 
quella precedente sia finita. Per fare questo, hanno deciso che vogliono che nella card della linea
il programma gestisca in questo modo:
- se c'è una sola presa tempo, allora va bene vedere quell'unica presa tempo, aggiungendo 
però un pulsante che permetta di aggiungerne una seconda;
- se c'è più di una presa tempo, la card deve visualizzare solo il conteggio delle prese tempo aperte
aperte su quella linea e ci deve essere un pulsante che rimanda ad una pagina html con 
l'elenco sotto forma di card delle prese tempo aperte con i relativi dettagli e un pulsante
per aprire la presa tempo.

'''



def home(request):
        return render(request, "dashboard.html")


def my_view(request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
                login(request, user)
                return render(request, "/dashboard.html")
        else:
                return render(request, "registration/login.html")


class ListaOrdiniView(FilterView):

        model = Tbldettaglioordini
        context_object_name = 'initial_orders'
        template_name = "listaordini.html"
        filterset_class = OrderFilter
        paginate_by = 30
        ordering = ['-iddettordine']



def cerca(request):
        if "q" in request.GET:

                querystring = request.GET.get("q")

                if len(querystring) == 0:
                        messages.error(request, 'Inserire un numero di ordine')
                        return redirect("dashboard")
                # Sistemare passando per elenco ordini filtrati
                if Tbldettaglioordini.objects.filter(idordine__nordine=querystring):
                        dettaglio = Tbldettaglioordini.objects.get(pk=querystring)
                        operatori_attivi = Tbltempi.objects.filter(iddettordine=dettaglio, orafine__isnull = True).order_by('-datatempo')
                        form=FormDettaglio(request.POST or None, instance = dettaglio)
                        context = {"dettaglio": dettaglio, "operatori_attivi": operatori_attivi, 'form':form}
                        if request.method == 'POST':
                                if form.is_valid():
                                        dettaglio_salvato = form.save(commit=False)
                                        dettaglio_salvato.save()
                                        return HttpResponseRedirect(dettaglio.get_absolute_url())
                        return render(request, "singolo_dettaglio.html", context)
                else:
                        messages.error(request, 'Il numero ordine digitato non esiste')
                        return redirect("dashboard")

        else:
                return render(request, "dashboard.html",)


class OperatorView(ListView):
        paginate_by = 10

        context_object_name = 'operator_list'
        queryset = Tbltempi.objects.all()

        template_name = "_operatori.html"



def apri_lavorazione(request, pk, id_linea):
        dettaglio = get_object_or_404(Tbldettaglioordini, pk=pk)
        linea = TblLineeLav.objects.get(id_linea=id_linea)
        
        dettaglio.inlavoro = True
        dettaglio.completato = False
        dettaglio.save()
        operatori_attivi = Tbltempi.objects.all().filter(orafine__isnull = True, iddettordine__exact=pk)
        form=FormDettaglio(request.POST or None, instance = dettaglio)

        if request.method == 'POST':
                # form=FormDettaglio(request.POST)
                if form.is_valid():
                        dettaglio_salvato = form.save(commit=False)
                        dettaglio_salvato.save()
                        return HttpResponseRedirect(dettaglio.get_absolute_url())
        else:

                form = FormDettaglio(instance=dettaglio)
        context = {"dettaglio": dettaglio, "operatori_attivi": operatori_attivi, "linea": linea, 'form': form}
        return render(request, "singolo_dettaglio.html", context)


def dashboard(request):
        tempimaster=tblTempiMaster.objects.filter(completato=False)        
        tempi_aperti_count=tblTempiMaster.objects.filter(inlavoro=True).count()        
        d=timezone.now().date()-timedelta(days=7)
        dettaglio_ordini = Tbldettaglioordini.objects.filter(inlavoro = True).order_by('-iddettordine')[:15]
        operatori_attivi = Tbltempi.objects.filter(orafine__isnull = True).order_by('-orainizio')[:15]
        ordini_in_lavoro = Tbldettaglioordini.objects.filter(inlavoro = True).count
        n_operatori = Tbltempi.objects.filter(orafine__isnull = True).count()        
        linee = TblLineeLav.objects.all()        
        linee_dettaglio_1=tblTempiMaster.objects.filter(completato=False).order_by('-datatempo')
        linee_dettaglio=linee_dettaglio_1.values('id_linea').order_by('id_linea').annotate(count=Count('id_linea'))        
        query_tempi = Tbltempi.objects.filter(orafine__isnull = False).filter(datatempo__gte=d).annotate(duration=ExpressionWrapper(
                F('orafine') - F('orainizio'), output_field=DurationField()))
        total_time = query_tempi.aggregate(total_time=Sum('duration'))
        sum_time=total_time.get('total_time')
        if sum_time is not None:
                days=sum_time.days*24
                seconds=sum_time.seconds
                hours=seconds//3600+days
                minutes=(seconds//60)%60
        else:
                days=0
                seconds=0
                hours=0
                minutes=0


        context = {"dettaglio_ordini": dettaglio_ordini,
                "operatori_attivi": operatori_attivi,
                "ordini_in_lavoro": ordini_in_lavoro,
                "n_operatori": n_operatori,
                "ore": hours,
                "minuti": minutes,
                "linee": linee,
                "linee_dettaglio": linee_dettaglio,
                "tempimaster": tempimaster,                
                "tempi_aperti_count": tempi_aperti_count
                }

        return render(request, "dashboard.html", context)


def view_single_line_open_times(request, id_linea):
        '''
        view aggiunta per vedere i tempi aperti su una singola linea 
        per poter selezionare quello da chiudere come da richiesta del 16/11/2022
        '''
        linea=TblLineeLav.objects.get(pk=id_linea)
        tempimaster=tblTempiMaster.objects.filter(inlavoro=True).filter(id_linea=linea)
        tempimaster_all=tblTempiMaster.objects.filter(inlavoro=False).filter(id_linea=linea).order_by('-datatempo')
        tempimaster_all_count=tblTempiMaster.objects.filter(inlavoro=False).filter(id_linea=linea).count
        
        # Paginazione tempi chiusi
        page_tempimaster_all = request.GET.get('page', 1)
        paginator_tempimaster_all = Paginator(tempimaster_all, 30)
        try:
                tempimaster_all_paginator = paginator_tempimaster_all.page(page_tempimaster_all)
        except PageNotAnInteger:
                tempimaster_all_paginator = paginator_tempimaster_all.page(1)
        except EmptyPage:
                tempimaster_all_paginator = paginator_tempimaster_all.page(paginator_tempimaster_all.num_pages)
                
        context={
                "linea":linea,
                "tempimaster": tempimaster,
                "tempimaster_all": tempimaster_all,
                "tempimaster_all_paginator": tempimaster_all_paginator,
                "tempimaster_all_count": tempimaster_all_count
                
        }
        return render(request, "single_line.html", context)

'''04/10/2023 - Eliminata perchè integrata nella view precedente'''        
# def view_all_tracked(request):
#         '''
#         view aggiunta per vedere tutte le prese tempo come da richiesta di Ivano
#         del 20/12/2022
#         '''
#         linee=TblLineeLav.objects.all()
#         #tempimaster=tblTempiMaster.objects.filter(inlavoro=True).filter(id_linea=linea)
#         tempimaster_all=tblTempiMaster.objects.filter(inlavoro=False).order_by('-datatempo')        
#         context={
#                 "linee":linee,                
#                 "tempimaster_all": tempimaster_all
#         }
#         return render(request, "archivio_prese_tempo.html", context)

def add_line_search_order(request, id_linea):
        linea=TblLineeLav.objects.get(id_linea=id_linea)  
        
        filterset = OrderFilter(request.GET, queryset=Tbldettaglioordini.objects.all().order_by('-iddettordine'))
        filtered_dett_ordini = filterset.qs
        #filterset = OrderFilter(request.GET, queryset=Tbldettaglioordini.objects.filter(iddettordine__lt=35000).order_by('-iddettordine'))
        #print("Ordini: " + str(Tbldettaglioordini.objects.all()))        
        
        paginator = Paginator(filtered_dett_ordini, 30)
        page = request.GET.get('page')
        try:
                filter = paginator.page(page)
        except PageNotAnInteger:
                filter = paginator.page(1)
        except EmptyPage:
                filter = paginator.page(paginator.num_pages)
        context={'linea': linea, 'filter':filterset, 'filter_paginated': filter}
        
        
        return render(request, 'add_line_search_order.html', context)



def visualizza_dettaglio(request, pk, id_linea, idtempomaster):
        dettaglio = get_object_or_404(Tbldettaglioordini, pk=pk)
        tempomaster=tblTempiMaster.objects.get(pk=idtempomaster)
        operatori_attivi = Tbltempi.objects.filter(iddettordine=dettaglio).order_by('-datatempo','-orainizio')#.order_by('orainizio')
        linea=TblLineeLav.objects.get(id_linea=id_linea)
        form=FormDettaglio(request.POST or None, instance = dettaglio)
        
        if request.method == 'POST':                
                if form.is_valid():
                        dettaglio_salvato = form.save(commit=False)
                        dettaglio_salvato.save()
                        url_match= reverse_lazy('gestioneordini:visualizza_dettaglio', kwargs={'pk': dettaglio.iddettordine, 'id_linea': linea.id_linea, 'tempomaster': tempomaster.pk})
                        return redirect(url_match)
                        
        else:

                form = FormDettaglio(instance=dettaglio)
                
        context = {"dettaglio": dettaglio, 
                "operatori_attivi": operatori_attivi, 
                "form": form, 
                "linea": linea,
                "tempomaster": tempomaster
                }
        return render(request, "singolo_dettaglio.html", context)




def mostra_operatori_linea(request, pk, id_linea, idtempomaster):
        # form_quantity = None
        # form_media_tempo = None

        linea = TblLineeLav.objects.get(id_linea=id_linea)
        tempomaster=tblTempiMaster.objects.get(pk=idtempomaster)
        pezzi_tempo_master=tempomaster.quantity
        print(f"pezzi_tempo_master: {pezzi_tempo_master}")
        # query_dettaglio = linea.get_line()
        data_chiusura_tempo=tempomaster.data_chiusura_tempo
        
        # Definisco la variabile 'componente' che mi servirà per i conteggi dei tempi
        if tempomaster.iddettordine.idcomponente:
                componente = tempomaster.iddettordine.idcomponente
        else:
                componente = tempomaster.iddettordine.idcollegamento
        
        form_quantity = QuantityModelForm(instance=tempomaster)
        form_note = NoteLineaModelForm(instance=tempomaster)
        form_media_tempo = FormMediaTempi(instance=tempomaster)
        
        dettaglio = get_object_or_404(Tbldettaglioordini, pk=pk)
        
        operatori_attivi=Tbltempi.objects.filter(idtempomaster=tempomaster.pk).order_by('-datatempo', '-orainizio')#.order_by('orainizio')
        tot_tempo=0
        tot_tempo_min_sec=0
        #tempo_medio=0
        for operatore in operatori_attivi:
                if tempomaster.completato:
                        if operatore.orafine:
                                ora_fine=time.strftime(operatore.orafine,"%H:%M:%S")
                                ora_inizio=get_sec(str(operatore.orainizio))
                                ora_fine=get_sec(str(ora_fine))                
                                tot_tempo+=(ora_fine)-(ora_inizio)
                                #tempo_medio=timedelta(seconds=round((tot_tempo/tempomaster.quantity)))
                                if tempomaster.completato and tempomaster.quantity:
                                        # Se il tempomaster risulta completato e ha una quantità,
                                        # ottengo il tempo_medio
                                        tempo_medio = timedelta(seconds=round((tot_tempo / tempomaster.quantity)))
                                        
                                else:
                                        # Altrimenti il tempo medio viene settato a 0
                                        tempo_medio = timedelta(seconds=0)
                
                
                else:
                        # Se il tempoMaster non è completato, tempo_medio e tot_tempo vengono settati a 0
                        tempo_medio=0
                        tot_tempo=0
                        
                # Ottengo il totale tempo di produzione in secondi
                tot_tempo_min_sec=timedelta(seconds=tot_tempo)
        
        # Ottengo la media tempo al pezzo
        if tot_tempo_min_sec:
                tot_tempo_min_sec_float = tot_tempo_min_sec.total_seconds()              
                tot_tempo_min_sec=timedelta(seconds=(tot_tempo_min_sec_float/pezzi_tempo_master))
                tot_tempo_min_sec = str(tot_tempo_min_sec).split('.')[0]
                
        

        if request.method == 'POST':
                print("request post: " + str(request))
                if 'formQuantity' in request.POST:
                        form_quantity=QuantityModelForm(request.POST, instance = tempomaster)
                        
                        if form_quantity.is_valid():
                                dettaglio_salvato = form_quantity.save(commit=False)
                                dettaglio_salvato.save()
                elif 'mediaTempiForm' in request.POST:
                        form_media_tempo = FormMediaTempi(request.POST, instance = tempomaster)
                        if form_media_tempo.is_valid():
                                media_tempo = form_media_tempo.save(commit=False)
                                media_tempo.save()
                else:
                        form_note=NoteLineaModelForm(request.POST or None, instance = tempomaster)
                        
                        if form_note.is_valid():
                                note_salvate = form_note.save(commit=False)
                                note_salvate.save()
                
                
                        
        else:
                
                form_quantity=QuantityModelForm(instance = tempomaster)
                form_note=NoteLineaModelForm(instance = tempomaster)
                form_media_tempo=FormMediaTempi(request.POST or None, instance=tempomaster)
        # Azzero la variabile tempo_medio in quanto ho già il dato in tot_tempo_min_sec
        tempo_medio = 0
        
        # Se il componente/collegamento ha un tempo medio associato
        if get_if_media_tempo(componente)[0]:
                messaggio_tempo = True
                
                # Controllo se tempo_medio è di tipo int e lo converto in timedelta
                if isinstance(tempo_medio, int):
                        tempo_medio = timedelta(seconds=tempo_medio)   
                        
                        
                if get_tempo_medio(tempo_medio, componente)[0]:
                        print("risultato funzione: " + str(get_tempo_medio(tempo_medio, componente)[0]))
                        print("tempomedio prima di trasformazione: " + str(tempo_medio))
                        
                        tempo_medio=get_tempo_medio(tempo_medio, componente)[1]
                        print("tempomedio dopo trasformazione: " + str(tempo_medio))
                        
                        check_tempo=True
                        # Ottengo il tempo massimo consentito (tempo nominale + tolleranza)
                        tempo_massimo_consentito=get_tempo_medio(tempo_medio, componente)[2]
                        # Lo tronco ai secondi
                        tempo_massimo_consentito= str(tempo_massimo_consentito).split('.')[0]                        
                        tolleranza_percentuale=get_tempo_medio(tempo_medio, componente)[3]
                        tot_tempo_min_sec = str(tot_tempo_min_sec).split('.')[0]
                        if tempo_massimo_consentito != '0:00:00':
                                if operatori_attivi:
                                        differenza_percentuale = get_perc_differenza(tot_tempo_min_sec, tempo_massimo_consentito, tempo_medio)
                                else:
                                        differenza_percentuale = 0
                        else:
                                differenza_percentuale = 0
                        
                else:
                        
                        check_tempo=False
                        tempo_massimo_consentito='Media non presente'
                        differenza_percentuale=0
                        tolleranza_percentuale=get_tempo_medio(tempo_medio, componente)[3]
                        
        else:
                messaggio_tempo = get_if_media_tempo(componente)[1]
                check_tempo=False
                tempo_massimo_consentito='Media non presente'
                tolleranza_percentuale=0
                differenza_percentuale=0
                
        if data_chiusura_tempo:
                tolleranza_percentuale=tempomaster.perc_tempo
                tempo_medio = get_tempo_nominale_registrato(tempomaster)[0]
                tempo_massimo_consentito = get_tempo_nominale_registrato(tempomaster)[1]
                tempo_massimo_consentito= str(tempo_massimo_consentito).split('.')[0]
                if tempo_massimo_consentito != '0:00:00':
                        if operatori_attivi:
                                differenza_percentuale = get_perc_differenza(tot_tempo_min_sec, tempo_massimo_consentito, tempo_medio)
                        else:
                                differenza_percentuale = 0
                else:
                        differenza_percentuale = 0
                
                
        
        
        
                
        context = {'linea': linea,                         
                'dettaglio': dettaglio,
                'operatori_attivi': operatori_attivi,
                'form_quantity': form_quantity,
                'form_note': form_note,
                'tempomaster': tempomaster,
                'tempo_medio': tempo_medio,
                'tot_tempo_min_sec': tot_tempo_min_sec,
                'check_tempo': check_tempo,
                'messaggio_tempo': messaggio_tempo,
                'tempo_massimo_consentito': tempo_massimo_consentito,
                'tolleranza_percentuale': tolleranza_percentuale,
                'differenza_percentuale': differenza_percentuale,
                'form_media_tempo': form_media_tempo,
                'data_chiusura_tempo': data_chiusura_tempo,
                
                
                }
        return render(request, 'singolo_dettaglio.html', context)

def add_master_time(request, pk, id_linea):
        
        linea=TblLineeLav.objects.get(id_linea=id_linea)
        dettaglio=Tbldettaglioordini.objects.get(iddettordine=pk)
        
        
        current_time = datetime.now() 
        initial_data = {
                'id_linea': id_linea,
                'iddettordine': str(dettaglio.iddettordine),
                'datatempo': current_time.strftime("%d-%m-%Y"),
        }
        
        form = FormMaster(request.POST or None, initial = initial_data)
        context={
                        'form': form,
                        'dettaglio': dettaglio,
                        'linea': linea,
                        
                }
        print("Sono qui_1")
        if request.method == 'POST':
                
                form_media_tempo=FormMediaTempi(request.POST or None)
                # form=FormDettaglio(request.POST)
                if form.is_valid():
                        
                        dettaglio_salvato = form.save()
                        tempomaster=tblTempiMaster.objects.get(pk=dettaglio_salvato.idtempomaster)                        
                        operatori_attivi=Tbltempi.objects.filter(idtempomaster=tempomaster.pk)                        
                        form_media_tempo=FormMediaTempi(request.POST or None, instance=tempomaster)
                        if request.method == 'POST':
                                form=QuantityModelForm(request.POST or None, instance = tempomaster)
                                # form=FormDettaglio(request.POST)
                                if form.is_valid():
                                        dettaglio_salvato = form.save(commit=False)
                                        dettaglio_salvato.save()
                                form_note=NoteLineaModelForm(request.POST or None, instance = tempomaster)
                                # form=FormDettaglio(request.POST)
                                if form_note.is_valid():
                                        note_salvate = form_note.save(commit=False)
                                        note_salvate.save()
                                        
                                        
                        else:
                                form=QuantityModelForm(instance = tempomaster)
                                form_note=NoteLineaModelForm(instance = tempomaster)
                                form_media_tempo=FormMediaTempi(request.POST or None, instance=tempomaster)
                                #
                                
                        context = {"dettaglio": dettaglio, 
                        "operatori_attivi": operatori_attivi,                          
                        "linea": linea,
                        "tempomaster": tempomaster,
                        "form_quantity": form,
                        "form_note": form_note,
                        "prova:" : False,
                        'form_media_tempo': form_media_tempo,
                        'tot_tempo_min_sec': 0,
                        'tempo_medio': 0,
                        'tempo_massimo_consentito': 0
                        }
                        # dettaglio_salvato.save()
                        
                        return render(request, "singolo_dettaglio.html", context)
        
                
        return render(request, "add_master.html", context)



def add_master_time_barcode(request, id_linea):  
        '''
        Aggiungere un ordine ad un time master usando il barcode
        '''      
        linea=TblLineeLav.objects.get(id_linea=id_linea)        
        
        if "q" in request.GET:
                querystring = request.GET.get("q")

                if len(querystring) == 0:
                        messages.error(request, 'Inserire un ordine')
                        return redirect('gestioneordini:add-to-line', id_linea=id_linea)
                
                # Controllo il barcode 
                if check_barcode(querystring, 'ordini')[0]==True:
                        querystring=check_barcode(querystring, 'ordini')[1]
                else:
                        messages.error(request, check_barcode(querystring, 'ordini')[1])
                        return redirect('gestioneordini:add-to-line', id_linea=id_linea)
                if Tbldettaglioordini.objects.filter(pk=querystring):
                        dettaglio=querystring
                        current_time = datetime.now() 
                        initial_data = {
                                'id_linea': id_linea,
                                'iddettordine': querystring,
                                'datatempo': current_time.strftime("%d-%m-%Y"),
                        }
                        
                        form = FormMaster(request.POST or None, initial = initial_data)
                        context={
                                'form': form,
                                'dettaglio': dettaglio,
                                'linea': linea,
                                
                        }
                        if request.method == 'POST':
                                # form=FormDettaglio(request.POST)
                                if form.is_valid():
                                        dettaglio_salvato = form.save()
                                        tempomaster=tblTempiMaster.objects.get(pk=dettaglio_salvato.idtempomaster)                        
                                        operatori_attivi=Tbltempi.objects.filter(idtempomaster=tempomaster.pk)                        
                                        if request.method == 'POST':
                                                form=QuantityModelForm(request.POST or None, instance = tempomaster)
                                                # form=FormDettaglio(request.POST)
                                                if form.is_valid():
                                                        dettaglio_salvato = form.save(commit=False)
                                                        dettaglio_salvato.save()
                                                form_note=NoteLineaModelForm(request.POST or None, instance = tempomaster)
                                                # form=FormDettaglio(request.POST)
                                                if form_note.is_valid():
                                                        note_salvate = form_note.save(commit=False)
                                                        note_salvate.save()
                                                        
                                        else:
                                                form=QuantityModelForm(instance = tempomaster)
                                                form_note=NoteLineaModelForm(instance = tempomaster)
                                        context = {"dettaglio": dettaglio, 
                                        "operatori_attivi": operatori_attivi,                          
                                        "linea": linea,
                                        "tempomaster": tempomaster,
                                        "form": form,
                                        "form_note": form_note
                                        }
                                        # dettaglio_salvato.save()
                                        return render(request, "singolo_dettaglio.html", context)
                else:
                        messages.error(request, 'Ordine inesistente')
                        return redirect('gestioneordini:add-to-line', id_linea=id_linea)

        return redirect('gestioneordini:add-master', pk=dettaglio, id_linea=id_linea)

def chiudi_lavorazione(request, pk, id_linea):
        dettaglio = get_object_or_404(tblTempiMaster, pk=pk)        
        print("Arrivato qui")
        linea = TblLineeLav.objects.get(id_linea=id_linea)
        operatori_attivi = Tbltempi.objects.all().filter(orafine__isnull = True, idtempomaster__exact=pk, id_linea__exact=id_linea)
        operatori = Tbltempi.objects.all().filter(idtempomaster__exact=pk, id_linea__exact=id_linea)
        dettaglio.inlavoro = False
        dettaglio.completato = True
        dettaglio.save()
        for operatore in operatori_attivi:

                current_time = datetime.now()
                close_time = current_time.strftime("%H:%M:")
                operatore.orafine = current_time
                operatore.save()
        
        # Calcolo il tempo medio
        tot_tempo=0
        for operatore in operatori: 
                ora_fine=time.strftime(operatore.orafine,"%H:%M:%S")
                ora_inizio=get_sec(str(operatore.orainizio))
                ora_fine=get_sec(str(ora_fine))                
                tot_tempo+=(ora_fine)-(ora_inizio)       
                
        if dettaglio.iddettordine.idcomponente:
                componente = dettaglio.iddettordine.idcomponente
        else:
                componente = dettaglio.iddettordine.idcollegamento
        tempo_medio = timedelta(seconds=round((tot_tempo / dettaglio.quantity)))
        
        # if get_if_media_tempo(componente)[0]:
        #         if get_tempo_medio(tempo_medio, componente)[0]:
        #                 check_tempo=True
        #                 print("Check Tempo: " + str(check_tempo))
        #                 dettaglio.tempo_massimo_consentito=get_tempo_medio(tempo_medio, componente)[0] 
        #                 dettaglio.ore_medie_lavorazione = get_tempo_nominale(componente)[0]
        #                 dettaglio.minuti_medi_lavorazione = get_tempo_nominale(componente)[1]
        #                 dettaglio.secondi_medi_lavorazione = get_tempo_nominale(componente)[2]
        #                 dettaglio.perc_tempo = get_tempo_nominale(componente)[3]
        #                 dettaglio.data_chiusura_tempo=date.today()
        #                 print(f'data_chiusura_tempo get_tempo_medio= True: {dettaglio.data_chiusura_tempo}')
        #                 dettaglio.tempo_conforme = "Tempo OK"
        #                 dettaglio.save()
        # else:
        #         print("Non esiste un tempo medio assegnato")
        #         dettaglio.ore_medie_lavorazione = get_tempo_nominale(componente)[0]
        #         dettaglio.minuti_medi_lavorazione = get_tempo_nominale(componente)[1]
        #         dettaglio.secondi_medi_lavorazione = get_tempo_nominale(componente)[2]
        #         dettaglio.perc_tempo = get_tempo_nominale(componente)[3]
        #         dettaglio.data_chiusura_tempo=date.today()
        #         print(f'data_chiusura_tempo get_tempo_medio= False: {dettaglio.data_chiusura_tempo}')
        #         dettaglio.tempo_conforme = "Tempo Non Conforme"
        #         dettaglio.save()
        
        # 07/07/2024 - Modificata per ottenere il tempo e salvarlo nell'istanza.
        check_tempo, messaggio_tempo = get_if_media_tempo(componente)
        if check_tempo:
                tempo_medio_check, tempo_medio, tempo_massimo_consentito, tolleranza_percentuale = get_tempo_medio(tempo_medio, componente)
    
                if tempo_medio_check:
                        print("Check Tempo: " + str(tempo_medio_check))
                        dettaglio.tempo_massimo_consentito = tempo_massimo_consentito
                        dettaglio.ore_medie_lavorazione, dettaglio.minuti_medi_lavorazione, dettaglio.secondi_medi_lavorazione, dettaglio.perc_tempo = get_tempo_nominale(componente)
                        dettaglio.data_chiusura_tempo = date.today()
                        print(f'data_chiusura_tempo get_tempo_medio= True: {dettaglio.data_chiusura_tempo}')
                        dettaglio.tempo_conforme = "Tempo OK"
                        dettaglio.save()
                else:
                        print("Tempo medio non conforme")
                        dettaglio.ore_medie_lavorazione, dettaglio.minuti_medi_lavorazione, dettaglio.secondi_medi_lavorazione, dettaglio.perc_tempo = get_tempo_nominale(componente)
                        dettaglio.data_chiusura_tempo = date.today()
                        print(f'data_chiusura_tempo get_tempo_medio= False: {dettaglio.data_chiusura_tempo}')
                        dettaglio.tempo_conforme = "Tempo Non Conforme"
                        dettaglio.save()
        else:
                print("Non esiste un tempo medio assegnato")
                dettaglio.ore_medie_lavorazione, dettaglio.minuti_medi_lavorazione, dettaglio.secondi_medi_lavorazione, dettaglio.perc_tempo = get_tempo_nominale(componente)
                dettaglio.data_chiusura_tempo = date.today()
                print(f'data_chiusura_tempo get_tempo_medio= False: {dettaglio.data_chiusura_tempo}')
                dettaglio.tempo_conforme = "Tempo Non Conforme"
                dettaglio.save()
                
        url_match= reverse_lazy('gestioneordini:visualizza_dettaglio_da_linea', kwargs={'pk':dettaglio.iddettordine.iddettordine, 'id_linea': linea.id_linea, 'idtempomaster': dettaglio.pk})      
        return redirect(url_match)
        


def aggiungi_operatore_attivo(request, pk, pk_linea, idtempomaster):

        tempomaster=tblTempiMaster.objects.get(pk=idtempomaster)
        current_time = datetime.now() 
        initial_data = {
                'idtempomaster': idtempomaster,
                'id_linea': pk_linea,
                'datatempo': current_time.strftime("%Y-%m-%d"),
                'orainizio': current_time.strftime("%H:%M:%S"),
                'idfase': 4

        }
        linea = TblLineeLav.objects.get(id_linea=pk_linea)
        dettaglio = Tbldettaglioordini.objects.get(pk=pk)
        
        if request.method == 'POST':
                form = TempoModelForm(request.POST, initial={"idlinea": pk_linea})
                
                if form.is_valid():
                        tempo = form.save(commit=False)
                        '''
                        Controllo se l'orario inserito è compreso 
                        nell'intervallo deciso da Ivano il 09/12/2022
                        '''
                        if check_time_range(tempo.orainizio, tempo.orafine)[0]==True:
                                messages.error(request, check_time_range(tempo.orainizio, tempo.orafine)[1])
                                context = {'form': form, 'dettaglio': dettaglio, 'linea': linea, 'tempomaster': tempomaster}
                                return render(request, 'creatempo.html', context)
                                
                        if Tbltempi.objects.filter(idoperatore=tempo.idoperatore, orafine__isnull=True):
                                tempo_aperto= Tbltempi.objects.get(idoperatore=tempo.idoperatore, orafine__isnull=True)
                                idtempo=tempo_aperto.idtempo
                                return redirect('gestioneordini:ask-for-close', idtempo=idtempo, iddettaglio=dettaglio.pk, pk_linea=linea.pk, idtempomaster=tempomaster.pk)
                                
                        tempo.iddettordine = dettaglio
                        dettaglio.inlavoro = True
                        dettaglio.completato = False
                        dettaglio.save()
                        tempo.save()
                                                
                        return redirect('gestioneordini:visualizza_dettaglio_da_linea', pk=pk, id_linea=pk_linea, idtempomaster=idtempomaster)
        
        else:
                form = TempoModelForm(instance=dettaglio, initial=initial_data)

        context = {
                'form': form, 
                'dettaglio': dettaglio,
                'linea': linea,
                'tempomaster': tempomaster
                }
        return render(request, 'creatempo.html', context)


def cerca_operatore(request, pk, pk_linea, idtempomaster):
        '''
        INSERIRE GLI OPERATORI DIRETTAMENTE CON BARCODE
        '''
        dettaglio = Tbldettaglioordini.objects.get(pk=pk)
        linea = TblLineeLav.objects.get(id_linea=pk_linea)
        tempomaster=get_object_or_404(tblTempiMaster, pk=idtempomaster)
        
        if "q" in request.GET:
                querystring = request.GET.get("q")

                if len(querystring) == 0:
                        messages.error(request, 'Inserire un operatore')
                        return redirect('gestioneordini:visualizza_dettaglio_da_linea', pk=pk, id_linea=pk_linea, idtempomaster=idtempomaster)
                
                # Controllo il barcode 
                if check_barcode(querystring, 'operatori')[0]==True:
                        querystring=check_barcode(querystring, 'operatori')[1]
                else:
                        messages.error(request, check_barcode(querystring, 'operatori')[1])
                        return redirect('gestioneordini:visualizza_dettaglio_da_linea', pk=pk, id_linea=pk_linea, idtempomaster=idtempomaster)
                
                if Tbloperatori.objects.filter(pk=querystring):
                        operatore = get_object_or_404(Tbloperatori, pk=querystring)
                        if Tbltempi.objects.filter(idoperatore=querystring, orafine__isnull=True):
                                tempo= Tbltempi.objects.get(idoperatore=querystring, orafine__isnull=True)
                                idtempo=tempo.idtempo
                                return redirect('gestioneordini:ask-for-close', idtempo=idtempo, iddettaglio=dettaglio.pk, pk_linea=linea.pk, idtempomaster=tempomaster.pk)
                                

                        elif Tbloperatori.objects.filter(idoperatore=querystring, dimesso = True):                                
                                messages.error(request, 'Operatore ' + str(operatore) + ' dimesso')
                                return redirect('gestioneordini:visualizza_dettaglio_da_linea', pk=pk, id_linea=pk_linea, idtempomaster=idtempomaster)
                                
                        else:
                                operatore = get_object_or_404(Tbloperatori, pk=querystring)
                                #fase=get_object_or_404(Tblfasi, pk=4)
                                linea=get_object_or_404(TblLineeLav, pk=pk_linea)
                                starttime=datetime.now().strftime("%H:%M:%S")
                                return redirect('gestioneordini:add-auto', pk=dettaglio.pk, id_operatore=querystring, id_linea=linea.pk, id_tempomaster=idtempomaster, starttime=starttime)

                                # current_time = datetime.now()
                                # open_time = current_time.strftime("%H:%M:")
                                # open_date = current_time.strftime("%Y-%m-%d")
                                # model = Tbltempi()
                                # model.iddettordine=dettaglio
                                # model.idoperatore=operatore
                                # model.idfase=fase
                                # model.datatempo=open_date
                                # model.orainizio=open_time
                                # model.id_linea=linea
                                # model.idtempomaster=tempomaster

                                # model.save()
                                # messages.success(request, 'Operatore ' + str(operatore) + ' aggiunto')                                
                                # return redirect('gestioneordini:visualizza_dettaglio_da_linea', pk=pk, id_linea=pk_linea, idtempomaster=idtempomaster)
                else:
                        messages.error(request, 'Operatore inesistente')
                        return redirect('gestioneordini:visualizza_dettaglio_da_linea', pk=pk, id_linea=pk_linea, idtempomaster=idtempomaster)


def aggiungi_operatore_auto(request, pk, id_operatore, id_linea, id_tempomaster, starttime=datetime.now()):
        '''
        View da richiamare per aggiungere un operatore automaticamente da barcode
        pk=chiave primaria dettaglio ordine
        '''
        dettaglio = Tbldettaglioordini.objects.get(pk=pk)
        operatore = get_object_or_404(Tbloperatori, pk=id_operatore)
        fase=get_object_or_404(Tblfasi, pk=4)
        linea=get_object_or_404(TblLineeLav, pk=id_linea)
        tempomaster=get_object_or_404(tblTempiMaster, pk=id_tempomaster)
        current_time = datetime.now()
        
        format = "%H:%M:%S"        
        open_time = datetime.strptime(starttime, format)         
        open_time = datetime.time(open_time)
        open_date = current_time.strftime("%Y-%m-%d")
        
       
        if check_time_range(open_time, open_time)[0]==True:
                messages.error(request, check_time_range(open_time, open_time)[1])                
                return redirect('gestioneordini:visualizza_dettaglio_da_linea', pk=pk, id_linea=id_linea, idtempomaster=id_tempomaster)
        
        model = Tbltempi()
        model.iddettordine=dettaglio
        model.idoperatore=operatore
        model.idfase=fase
        model.datatempo=open_date
        model.orainizio=open_time
        model.id_linea=linea
        model.idtempomaster=tempomaster

        model.save()
        messages.success(request, 'Operatore ' + str(operatore) + ' aggiunto')        
        return redirect('gestioneordini:visualizza_dettaglio_da_linea', pk=pk, id_linea=id_linea, idtempomaster=id_tempomaster)
        

# view di aggiornamento operatori
def aggiorna_operatore_attivo(request, pk, iddett):        
        context ={}        
        obj = get_object_or_404(Tbltempi, pk = pk)
        tempomaster=tblTempiMaster.objects.get(pk=obj.idtempomaster.idtempomaster)
        linea = TblLineeLav.objects.get(id_linea=obj.id_linea.id_linea)
        dettaglio = Tbldettaglioordini.objects.get(iddettordine=iddett)        
        
        form = TempoModelForm(request.POST or None, instance = obj)
        
        if form.is_valid():                                
                tempo = form.save(commit=False)
                tempo.iddettordine = dettaglio
                
                form.save()
                return redirect('gestioneordini:visualizza_dettaglio_da_linea', pk=dettaglio.iddettordine, id_linea=linea.id_linea, idtempomaster=tempomaster.pk)
        
        context = {'form': form, 'dettaglio': dettaglio, 'linea': linea, 'tempomaster': tempomaster}
        return render(request, 'creatempo.html', context)

def chiudi_operatore(request, idtempo):
        dettaglio = get_object_or_404(Tbltempi, idtempo=idtempo)        
        linea = dettaglio.id_linea
        orainizio=dettaglio.orainizio        
        tempomaster=tblTempiMaster.objects.get(pk=dettaglio.idtempomaster.pk) 
        current_time = datetime.time(datetime.now())
        
        
        if check_end_time(current_time,orainizio)[0]==True:
                messages.error(request, check_end_time(current_time,orainizio)[1])                
                url_match= reverse_lazy('gestioneordini:visualizza_dettaglio_da_linea', kwargs={'pk':dettaglio.iddettordine.iddettordine, 'id_linea': linea.id_linea, 'idtempomaster': tempomaster.pk})      
                return redirect(url_match)
        
        dettaglio.orafine = current_time
        
        dettaglio.save()
        url_match= reverse_lazy('gestioneordini:visualizza_dettaglio_da_linea', kwargs={'pk':dettaglio.iddettordine.iddettordine, 'id_linea': linea.id_linea, 'idtempomaster': tempomaster.pk})      
        return redirect(url_match)


def delete_operatore(request, idtempo): 
        deleteobject = get_object_or_404(Tbltempi, idtempo = idtempo)        
        dettaglio=deleteobject.iddettordine           
        linea = deleteobject.id_linea  
        tempomaster=deleteobject.idtempomaster      
        deleteobject.delete()
        url_match= reverse_lazy('gestioneordini:visualizza_dettaglio_da_linea', kwargs={'pk':dettaglio.pk, 'id_linea': linea.id_linea, 'idtempomaster': tempomaster.pk})      
        return redirect(url_match)


def delete_tempo_master(request, pk):        
        '''
        Cancello il tempo master e in cascade i corrispettivi TblTempi
        '''
        deleteobject = get_object_or_404(tblTempiMaster, pk = pk)
        deleteobject.delete()
        return redirect('gestioneordini:dashboard')


def update_quantity_tempo_master(request, pk):        
        '''
        Aggiorno la quantità della presa tempo
        '''
                
        obj = get_object_or_404(tblTempiMaster, pk = pk)
                
        
        form = QuantityModelForm(request.POST or None, instance = obj)
        
        tempo = form.save(commit=False)                
                
        tempo.save()
        
        return redirect('gestioneordini:visualizza_dettaglio_da_linea', pk=obj.iddettordine.iddettordine, id_linea=obj.id_linea.id_linea, idtempomaster=obj.pk)


def update_line_note_tempo_master(request, pk):        
        '''
        Aggiorno le note da linea
        '''
                
        obj = get_object_or_404(tblTempiMaster, pk = pk)
        form = NoteLineaModelForm(request.POST or None, instance = obj)        
        tempo = form.save(commit=False)
        tempo.save()
        
        return redirect('gestioneordini:visualizza_dettaglio_da_linea', pk=obj.iddettordine.iddettordine, id_linea=obj.id_linea.id_linea, idtempomaster=obj.pk)
        

class OpenTimeView(ListView):

        model = tblTempiMaster        
        template_name = "tempi_aperti.html"        
        paginate_by = 15
        ordering = ['-datatempo']      

        def get_queryset(self):
                object_list = tblTempiMaster.objects.filter(inlavoro=True).order_by('datatempo', 'pk')               
                return object_list


def ask_for_close_operator(request, idtempo, iddettaglio, pk_linea, idtempomaster):
        '''
        View da chiamare in caso di operatore occupato
        idtempo=pk del tempo aperto relativo all'operatore
        iddettaglio=pk del dettaglio da passare per tornare alla pagina precedente
        pk_linea=pk della linea da passare per tornare alla pagina precedente
        idtempomaster=pk del tempomaster da passare per tornare alla pagina precedente
        '''
        dettaglio = Tbldettaglioordini.objects.get(pk=iddettaglio)
        linea = TblLineeLav.objects.get(id_linea=pk_linea)
        tempomaster=get_object_or_404(tblTempiMaster, pk=idtempomaster)
        tempo = get_object_or_404(Tbltempi, pk = idtempo)
        operatore = get_object_or_404(Tbloperatori, pk=tempo.idoperatore.pk)
        current_time = datetime.now() 
        initial_data = {
                'orafine': current_time.strftime("%H:%M:%S"),
        }
        
        form = AskForCloseModelForm(request.POST or None, instance = tempo, initial=initial_data)
        
        if form.is_valid():                
                tempo = form.save(commit=False)
                
                
                if check_time_range(tempo.orafine, tempo.orafine)[0]==True:
                        messages.error(request, check_time_range(tempo.orafine, tempo.orafine)[1])                
                        context = {'form': form, 'dettaglio': dettaglio, 'linea': linea, 'tempomaster': tempomaster, 'tempo': tempo}                        
                        return render(request, 'ask_for_close.html', context)
                starttime=tempo.orafine
                tempo.save()                             
                return redirect('gestioneordini:add-auto', pk=dettaglio.pk, id_operatore=operatore.pk, id_linea=linea.pk, id_tempomaster=idtempomaster,starttime=starttime)
        
        context = {'form': form, 'dettaglio': dettaglio, 'linea': linea, 'tempomaster': tempomaster, 'tempo': tempo}
        return render(request, 'ask_for_close.html', context)
        

'''
Custom 404 template
'''
def page_not_found_view(request, exception):
        return render(request, 'errors/404.html', status=404)






