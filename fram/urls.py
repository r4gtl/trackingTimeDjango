
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('gestioneordini.urls')),
    path('core/', include('core.urls')),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')), # importa tutti i link per la gestione degli accounts
    
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = "gestioneordini.views.page_not_found_view"