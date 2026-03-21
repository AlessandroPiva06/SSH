from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('componenti.urls')),
    path('api/', include('magazzino.urls')),
    path('api/', include('liste.urls')),
    path('api/auth/', include('utenti.urls')),  # ← aggiungi questa
]