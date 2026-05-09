from django.contrib import admin
from .models import Utente, LogAzione

admin.site.register(LogAzione)
admin.site.register(Utente)