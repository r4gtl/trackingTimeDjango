from django.forms.forms import Form
from django.forms.models import ModelChoiceField
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.views.generic.list import ListView
from django.urls import reverse_lazy, reverse
from django.db.models import Count, Q, F, DurationField, ExpressionWrapper, Sum
from django.core.paginator import Paginator
from django_filters.views import FilterView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .models import Qryoperatoriattivi, Qryordiniiniziale, TblLineeLav, Tbldettaglioordini, Tblfasi, Tbloperatori, Tbltempi
from .filters import OrderFilter
from .forms import FormDettaglio, TempoModelForm
from datetime import datetime, time, timedelta
from django.contrib import messages
from django.utils import timezone


# Create your views here.





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
        
        # model = Qryordiniiniziale
        model = Tbldettaglioordini

        context_object_name = 'initial_orders'
        template_name = "listaordini.html"
        filterset_class = OrderFilter
        paginate_by = 30  
        ordering = ['-iddettordine']
        # queryset = Tbldettaglioordini.objects.order_by('-iddettordine')[:1000]




def visualizza_dettaglio(request, pk):
        dettaglio = get_object_or_404(Tbldettaglioordini, pk=pk)
        operatori_attivi = Tbltempi.objects.filter(iddettordine=dettaglio, orafine__isnull = True).order_by('-datatempo')
        form=FormDettaglio(request.POST or None, instance = dettaglio)
        
        if request.method == 'POST':
                # form=FormDettaglio(request.POST)
                if form.is_valid():
                        dettaglio_salvato = form.save(commit=False)
                        dettaglio_salvato.save()
                        return HttpResponseRedirect(dettaglio.get_absolute_url())
        else:
                
                form = FormDettaglio(instance=dettaglio)
        context = {"dettaglio": dettaglio, "operatori_attivi": operatori_attivi, 'form':form}        
        return render(request, "singolo_dettaglio.html", context)



def cerca(request):
        if "q" in request.GET:
                querystring = request.GET.get("q")
                print(querystring)
                if len(querystring) == 0:
                        return redirect("/cerca/")
                dettaglio = get_object_or_404(Tbldettaglioordini, pk=querystring)
                operatori_attivi = Tbltempi.objects.filter(iddettordine=dettaglio, orafine__isnull = True).order_by('-datatempo')
                form=FormDettaglio(request.POST or None, instance = dettaglio)
                context = {"dettaglio": dettaglio, "operatori_attivi": operatori_attivi, 'form':form}        
                if request.method == 'POST':
        #                 # form=FormDettaglio(request.POST)
                        if form.is_valid():
                                dettaglio_salvato = form.save(commit=False)
                                dettaglio_salvato.save()
                                return HttpResponseRedirect(dettaglio.get_absolute_url())
                return render(request, "singolo_dettaglio.html", context)
        else:
                return render(request, "singolo_dettaglio.html",)


# def visualizza_dettaglio(request, pk):
#         dettaglio = get_object_or_404(Tbldettaglioordini, pk=pk)
#         operatori_attivi = Tbltempi.objects.filter(iddettordine=dettaglio, orafine__isnull = True).order_by('-datatempo')
#         form=FormDettaglio(request.POST or None, instance = dettaglio)
        
#         if request.method == 'POST':
#                 # form=FormDettaglio(request.POST)
#                 if form.is_valid():
#                         dettaglio_salvato = form.save(commit=False)
#                         dettaglio_salvato.save()
#                         return HttpResponseRedirect(dettaglio.get_absolute_url())
#         else:
#                 if "q" in request.GET:
#                         querystring = request.GET.get("q")
#                         print("QueryString:" + str(querystring))
#                         dettaglio = get_object_or_404(Tbldettaglioordini, pk=int(querystring))
#                         print("Prima QueryString:" + str(querystring))
#                         # return HttpResponseRedirect(dettaglio.get_absolute_url())
#                         if len(querystring) == 0:
#                                 print("Non Esiste")

                
#                 print("Secondo print: " + str(dettaglio))

#                 form = FormDettaglio(instance=dettaglio)
#         context = {"dettaglio": dettaglio, "operatori_attivi": operatori_attivi, 'form':form}        
#         return render(request, "singolo_dettaglio.html", context)


        
# def cerca(request):
#         if "q" in request.GET:
#                 querystring = request.GET.get("q")
#                 print(querystring)
#                 if len(querystring) == 0:
#                         return redirect("/cerca/")
#                 dettaglio = get_object_or_404(Tbldettaglioordini, pk=int(querystring))
#                 print(querystring)
#                 context = {"dettaglio": dettaglio,}
#                 return render(request, 'cerca.html', context)
#         else:
#                 return render(request, 'cerca.html')







class OperatorView(ListView):
        paginate_by = 10

        context_object_name = 'operator_list'  
        queryset = Tbltempi.objects.all()
        
        template_name = "_operatori.html"



def dashboard(request):
        dettaglio_ordini = Tbldettaglioordini.objects.filter(inlavoro = True).order_by('-iddettordine')[:15]
        operatori_attivi = Tbltempi.objects.filter(orafine__isnull = True).order_by('-orainizio')[:15]             
        ordini_in_lavoro = Tbldettaglioordini.objects.filter(inlavoro = True).count
        n_operatori = Tbltempi.objects.filter(orafine__isnull = True).count
        
        d=timezone.now().date()-timedelta(days=7)
        
        query_tempi = Tbltempi.objects.filter(orafine__isnull = False).filter(datatempo__gte=d).annotate(duration=ExpressionWrapper(
                F('orafine') - F('orainizio'), output_field=DurationField()))
        total_time = query_tempi.aggregate(total_time=Sum('duration'))
        sum_time=total_time.get('total_time')        
        if sum_time is not None:        
                days=sum_time.days*60 
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
                "minuti": minutes}
        
        return render(request, "dashboard.html", context)




def home(request):
        return render(request, "dashboard.html")

def chiudi_operatore(request, pk):
        obj = get_object_or_404(Tbltempi, pk=pk) 
        post= obj.iddettordine            
        current_time = datetime.now()
        close_time = current_time.strftime("%H:%M:")
        obj.orafine = close_time
        obj.save()
        
        return HttpResponseRedirect(post.get_absolute_url())

def chiudi_lavorazione(request, pk):
        dettaglio = get_object_or_404(Tbldettaglioordini, pk=pk) 
        operatori_attivi = Tbltempi.objects.all().filter(orafine__isnull = True, iddettordine__exact=pk)
        dettaglio.inlavoro = False
        dettaglio.completato = True
        dettaglio.save() 
        for operatore in operatori_attivi:
                
                current_time = datetime.now()
                close_time = current_time.strftime("%H:%M:")
                operatore.orafine = close_time
                operatore.save()
        
        return HttpResponseRedirect(dettaglio.get_absolute_url())

def apri_lavorazione(request, pk):
        dettaglio = get_object_or_404(Tbldettaglioordini, pk=pk) 
        dettaglio.inlavoro = True
        dettaglio.completato = False
        dettaglio.save()  
        
        return HttpResponseRedirect(dettaglio.get_absolute_url())


def cerca_operatore(request, pk):
        current_user = request.user
                
        if current_user.username == "Linea_1":
                pk_linea = 1                
        elif current_user.username == "Linea_2":
                pk_linea = 2
        elif current_user.username == "Linea_3":
                pk_linea = 3
        elif current_user.username == "Linea_4":
                pk_linea = 4
        elif current_user.username == "Linea_5":
                pk_linea = 5
        else:
                pk_linea = 1

        
        dettaglio = Tbldettaglioordini.objects.get(pk=pk)
        if "q" in request.GET:
                querystring = request.GET.get("q")
                
                if len(querystring) == 0:
                        return redirect("/cerca/")
                if Tbltempi.objects.filter(idoperatore=querystring, orafine__isnull=True):
                
                        context= {'dettaglio_attivo': dettaglio, 'origine': 'prova'}
                        return render(request, 'messaggio_operatore_attivo.html', context)

                elif Tbloperatori.objects.filter(idoperatore=querystring, dimesso = True):
                        context= {'dettaglio_attivo': dettaglio, 'origine': 'prova1'}
                        return render(request, 'messaggio_operatore_attivo.html', context)
                                
                else:                                
                        operatore = get_object_or_404(Tbloperatori, pk=querystring)   
                        fase=get_object_or_404(Tblfasi, pk=4)                       
                        linea=get_object_or_404(TblLineeLav, pk=pk_linea)                       
                        

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
                        
                        model.save()
                        
                        return HttpResponseRedirect(dettaglio.get_absolute_url())           



def aggiungi_operatore_attivo(request, pk):

        dettaglio = Tbldettaglioordini.objects.get(pk=pk)        
        if request.method == 'POST':
                form = TempoModelForm(request.POST)

                if form.is_valid():                       
                        tempo = form.save(commit=False)
                        tempo.iddettordine = dettaglio                        
                        dettaglio.inlavoro = True
                        dettaglio.completato = False
                        dettaglio.save()                        
                        tempo.save()

                        return HttpResponseRedirect(dettaglio.get_absolute_url())
        else:
                form = TempoModelForm(instance=dettaglio)
                form.fields['idoperatore'].queryset=Tbloperatori.objects.filter(dimesso__iexact="false").exclude(tbltempi__orafine__isnull=True).order_by('cognome')

        context = {'form': form, 'dettaglio': dettaglio}
        return render(request, 'creatempo.html', context)


# def aggiorna_operatore(request, pk):
#                 # dictionary for initial data with
#         # field names as keys
#         dettaglio = get_object_or_404(Tbldettaglioordini, pk=pk)
#         print("Prova")
#         context ={}
        
#         # pass the object as instance in form
#         form = TempoModelForm(request.POST or None, instance = dettaglio)
#         # form = TempoModelForm(initial={'dettaglio': dettaglio})
#         # save the data from the form and
#         # redirect to detail_view
        
#         if form.is_valid():
                
#                 # form = TempoModelForm(request.POST)
#                 form.save()
#                 # post = obj.iddettordine 
#                 # return reverse_lazy( 'visualizza_dettaglio', kwargs={'pk': dettaglio})
#                 return HttpResponseRedirect(dettaglio.get_absolute_url())
#                 # return render(request, "/dashboard.html")
        
#         # add form dictionary to context
#         # context["form"] = form        
#         # context = {'form': form, 'dettaglio': dettaglio}
#         context = {'form': form, 'dettaglio': dettaglio }
#         return render(request, "creatempo.html", context)

class TempoUpdateView(UpdateView):
        model = Tbltempi
        form_class=TempoModelForm        
        template_name = 'creatempo.html'        

        def get_success_url(self):
                post = self.object.iddettordine 
                return reverse_lazy( 'visualizza_dettaglio', kwargs={'pk': post.iddettordine})
        
        def get_initial(self):
                return {'datatempo': datetime.date.today}



class CancellaOperatore(DeleteView):
        model = Tbltempi
        def get_success_url(self):
                post = self.object.iddettordine 
                return reverse_lazy( 'visualizza_dettaglio', kwargs={'pk': post.iddettordine})






