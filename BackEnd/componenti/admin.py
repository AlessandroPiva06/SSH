from django.contrib import admin
from .models import Componente, Famiglia, Tag, Locazione

admin.site.register(Componente)
admin.site.register(Famiglia)
admin.site.register(Tag)
admin.site.register(Locazione)