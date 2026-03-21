from rest_framework import viewsets
from .models import ListaEsperienza, ListaAcquisti
from .serializers import ListaEsperienzaSerializer, ListaAcquistiSerializer

class ListaEsperienzaViewSet(viewsets.ModelViewSet):
    queryset = ListaEsperienza.objects.all()
    serializer_class = ListaEsperienzaSerializer

class ListaAcquistiViewSet(viewsets.ModelViewSet):
    queryset = ListaAcquisti.objects.all()
    serializer_class = ListaAcquistiSerializer