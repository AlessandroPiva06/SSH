from django.db import models
from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Componente, Famiglia, Tag, Locazione
from .serializers import ComponenteSerializer, FamigliaSerializer, TagSerializer, LocazioneSerializer

class PermessoPerRuolo(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return request.user.approvato
        return request.user.ruolo in ['admin', 'tecnico']

class ComponenteViewSet(viewsets.ModelViewSet):
    queryset = Componente.objects.all()
    serializer_class = ComponenteSerializer
    permission_classes = [PermessoPerRuolo]

    # Filtering per campi esatti
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['famiglia', 'tag', 'locazione', 'is_scorta']

    # Ricerca testuale
    search_fields = ['nome', 'famiglia__nome', 'tag__nome']

    # Ordinamento
    ordering_fields = ['nome', 'quantita', 'quantita_minima']
    ordering = ['nome']  # default

    # Endpoint extra: /api/componenti/sotto_scorta/
    @action(detail=False, methods=['get'])
    def sotto_scorta(self, request):
        componenti = Componente.objects.filter(quantita__lte=models.F('quantita_minima'))
        serializer = self.get_serializer(componenti, many=True)
        return Response(serializer.data)

class FamigliaViewSet(viewsets.ModelViewSet):
    queryset = Famiglia.objects.all()
    serializer_class = FamigliaSerializer
    permission_classes = [PermessoPerRuolo]

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [PermessoPerRuolo]

class LocazioneViewSet(viewsets.ModelViewSet):
    queryset = Locazione.objects.all()
    serializer_class = LocazioneSerializer
    permission_classes = [PermessoPerRuolo]