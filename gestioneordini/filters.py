from django.db.models.fields import BooleanField
import django_filters
from django import forms
from django_filters import DateFilter
from django_filters.filters import BooleanFilter
from .models import *
from crispy_forms.bootstrap import InlineRadios



class OrderFilter(django_filters.FilterSet):
        
        n_ordine=django_filters.CharFilter(field_name='idordine__nordine', lookup_expr='icontains', widget=forms.TextInput(attrs={'style': 'width: 90%; margin-left: 5%'}))        
        cod_comp=django_filters.CharFilter(field_name='idcomponente__codice', lookup_expr='icontains', widget=forms.TextInput(attrs={'style': 'width: 90%; margin-left: 7%'}))        
        cod_coll=django_filters.CharFilter(field_name='idcollegamento__codicecollegamento' , lookup_expr='icontains', widget=forms.TextInput(attrs={'style': 'width: 90%; margin-left: 7%'}))        
        ncommessa=django_filters.CharFilter(field_name='ncommessa' , lookup_expr='icontains', widget=forms.TextInput(attrs={'style': 'width: 90%; margin-left: 7%'}))
        idcliente=forms.ModelChoiceField(label="Item Choices", queryset=Tblclienti.objects.all(), required=True)
        class Meta:
            # model = Qryordiniiniziale
            model = Tbldettaglioordini
            fields = ['idordine__idcliente', 'n_ordine', 'ncommessa', 'cod_comp', 'cod_coll', 'inlavoro', 'completato']
            filter_overrides = {
                models.CharField: {
                    'filter_class': django_filters.CharFilter,
                    'extra': lambda f: {
                        'lookup_expr': 'icontains',
                        'widget' : forms.TextInput(attrs={'style': 'width: 90%; margin-left: 5%'})
                        
                    },
                },
                models.BooleanField: {
                    'filter_class': django_filters.BooleanFilter,
                    'extra': lambda f: {
                        
                        'widget' : forms.CheckboxInput(attrs={'class': 'form-check-input', 'style': 'align-center'})
                    },
                }
            }
            widgets = {
                'inlavoro': forms.RadioSelect(attrs={'class': 'form-check-input'}),
                'completato': BooleanFilter(attrs={'class': 'form-control'})

            }
        
        exclude = ['id_dett_ord', 'idcollegamento']

        