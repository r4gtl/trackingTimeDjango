from django.urls import path
from . import views

app_name="core"

urlpatterns = [
    path('core/pdf_view/', views.ViewPDF.as_view(), name="pdf_view"),
    
]