from django.urls import path
from . import views

app_name="core"

urlpatterns = [
    path('core/pdf_view/', views.ViewPDF.as_view(), name="pdf_view"),
    path('print_grid_label/<int:iddettordine>/', views.view_grid_labels, name="print_grid_label"),
    
]