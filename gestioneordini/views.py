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
        AskForCloseModelForm
)
from datetime import datetime, time, timedelta, date
from django.contrib import messages
from django.utils import timezone
from .utilities import check_barcode


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


'''
In data 04/09/2022 Vanessa dice che devono prendere più tempi per una sola riga di dettaglio.
Questo comporta il dover gestire il tutto con una nuova tabella (tblTempiMaster), in cui
mettiamo in collegamento i tempi e il dettaglio ordini. 
'''
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


def add_line_search_order(request, id_linea):
        linea=TblLineeLav.objects.get(id_linea=id_linea)  
        
        filterset = OrderFilter(request.GET, queryset=Tbldettaglioordini.objects.all().order_by('-iddettordine'))        
        paginator = Paginator(filterset.qs, 30)
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
        operatori_attivi = Tbltempi.objects.filter(iddettordine=dettaglio).order_by('-datatempo')
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
        linea = TblLineeLav.objects.get(id_linea=id_linea)
        tempomaster=tblTempiMaster.objects.get(pk=idtempomaster)
        
        query_dettaglio = linea.get_line()
        
        
        dettaglio = get_object_or_404(Tbldettaglioordini, pk=pk)
        
        operatori_attivi=Tbltempi.objects.filter(idtempomaster=tempomaster.pk).order_by('-datatempo')
        
        if request.method == 'POST':
                form=QuantityModelForm(request.POST or None, instance = tempomaster)
                # form=FormDettaglio(request.POST)
                if form.is_valid():
                        dettaglio_salvato = form.save(commit=False)
                        dettaglio_salvato.save()
                        
        else:
                form=QuantityModelForm(instance = tempomaster)
                
                
        
        context = {'linea': linea,                         
                'dettaglio': dettaglio,
                'operatori_attivi': operatori_attivi,
                'form': form,
                'tempomaster': tempomaster
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
                                        
                        else:
                                form=QuantityModelForm(instance = tempomaster)
                        context = {"dettaglio": dettaglio, 
                        "operatori_attivi": operatori_attivi,                          
                        "linea": linea,
                        "tempomaster": tempomaster,
                        "form": form
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
                                                        
                                        else:
                                                form=QuantityModelForm(instance = tempomaster)
                                        context = {"dettaglio": dettaglio, 
                                        "operatori_attivi": operatori_attivi,                          
                                        "linea": linea,
                                        "tempomaster": tempomaster,
                                        "form": form
                                        }
                                        # dettaglio_salvato.save()
                                        return render(request, "singolo_dettaglio.html", context)
                else:
                        messages.error(request, 'Ordine inesistente')
                        return redirect('gestioneordini:add-to-line', id_linea=id_linea)

        return redirect('gestioneordini:add-master', pk=dettaglio, id_linea=id_linea)

def chiudi_lavorazione(request, pk, id_linea):
        dettaglio = get_object_or_404(tblTempiMaster, pk=pk)        
                
        linea = TblLineeLav.objects.get(id_linea=id_linea)
        operatori_attivi = Tbltempi.objects.all().filter(orafine__isnull = True, idtempomaster__exact=pk, id_linea__exact=id_linea)
        dettaglio.inlavoro = False
        dettaglio.completato = True
        dettaglio.save()
        for operatore in operatori_attivi:

                current_time = datetime.now()
                close_time = current_time.strftime("%H:%M:")
                operatore.orafine = current_time
                operatore.save()
        
        return redirect('gestioneordini:dashboard')


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
                                return redirect('gestioneordini:add-auto', pk=dettaglio.pk, id_operatore=querystring, id_linea=linea.pk, id_tempomaster=idtempomaster)

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


def aggiungi_operatore_auto(request, pk, id_operatore, id_linea, id_tempomaster):
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
        open_time = current_time.strftime("%H:%M:")
        open_date = current_time.strftime("%Y-%m-%d")
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
        return redirect('gestioneordini:visualizza_dettaglio_da_linea', pk=pk, id_linea=4, idtempomaster=id_tempomaster)
        

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
                print("data:" + str(tempo.datatempo))
                form.save()
                return redirect('gestioneordini:visualizza_dettaglio_da_linea', pk=dettaglio.iddettordine, id_linea=linea.id_linea, idtempomaster=tempomaster.pk)
                
        context = {'form': form, 'dettaglio': dettaglio, 'linea': linea, 'tempomaster': tempomaster}
        return render(request, 'creatempo.html', context)

def chiudi_operatore(request, idtempo):
        dettaglio = get_object_or_404(Tbltempi, idtempo=idtempo)        
        linea = dettaglio.id_linea
        tempomaster=tblTempiMaster.objects.get(pk=dettaglio.idtempomaster.pk)        
        current_time = datetime.now()        
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
        print("Ecolo")
        #if form.is_valid():
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
                tempo.save()              
                return redirect('gestioneordini:add-auto', pk=dettaglio.pk, id_operatore=operatore.pk, id_linea=linea.pk, id_tempomaster=idtempomaster)
        
        context = {'form': form, 'dettaglio': dettaglio, 'linea': linea, 'tempomaster': tempomaster, 'tempo': tempo}
        return render(request, 'ask_for_close.html', context)
        

'''
Custom 404 template
'''
def page_not_found_view(request, exception):
        return render(request, 'errors/404.html', status=404)




