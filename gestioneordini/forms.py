from django import forms
import datetime
from django.utils.safestring import mark_safe
from .models import Qryordiniiniziale, Tbldettaglioordini, Tbltempi, Tbloperatori



class FormDettaglio(forms.ModelForm):
    
    
    class Meta:
        model = Tbldettaglioordini
        fields = [
            "noteconteggi",
            "quantitatempo",
            "completato"
            ]
        
        widgets = {        
            "noteconteggi": forms.Textarea(attrs={'class': 'textarea', 'cols': 40, 'rows': 4, 'placeholder': 'Inserisci le annotazioni' },  ), 
            "quantitatempo": forms.NumberInput(attrs={'class': 'input', 'style': 'text-align:right;'},  ), 


            
        }

        labels = {
            "quantitatempo": mark_safe("<p>Quantità Tempo</p>"),
            "noteconteggi": mark_safe("<p>Note su Conteggi</p>"),
        }


class TempoModelForm(forms.ModelForm):
    
    class Meta:
        model = Tbltempi

        fields = ["idtempo","id_linea", "idoperatore", "idfase", "datatempo", "orainizio", "orafine", "quantitatemporiparazione", "note", ]
                
        widgets = {             
            # "datatempo": forms.DateInput(attrs={'class':'form-control', 'value': datetime.date.today().strftime("%d-%m-%Y"), 'type': 'date'}),
            "idtempo": forms.HiddenInput(),
            "datatempo": forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'type': 'date'}),
            "orainizio": forms.TimeInput(format=('%H:%M:%S'),attrs={'type': 'time'}),
            "orafine": forms.TimeInput(format=('%H:%M:%S'), attrs={'type': 'time'}),            
            "note": forms.Textarea(attrs={'cols': 80, 'rows': 2}),
            # "idoperatore": forms.ChoiceField(choices = Tbloperatori.objects.filter(dimesso__iexact="false").exclude(tbltempi__orafine__isnull=True).order_by('cognome'), initial=0)
            
        }
        labels = {
            "id_linea": "Linea",
            "idoperatore": "Operatore",
            "idfase": "Fase",
            "datatempo": "Data"

        }
        
    def __init__(self, *args, **kwargs):
        super(TempoModelForm, self).__init__(*args, **kwargs)                
        self.fields['idoperatore'].queryset = Tbloperatori.objects.filter(dimesso__iexact="false").order_by('cognome')# or something else
        self.fields['idoperatore'].widget.attrs.update({'autofocus': 'autofocus'})
        