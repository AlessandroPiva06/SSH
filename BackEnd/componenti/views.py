from rest_framework import viewsets, permissions
from .models import Componente, Famiglia, Tag, Locazione
from .serializers import ComponenteSerializer, FamigliaSerializer, TagSerializer, LocazioneSerializer

class PermessoPerRuolo(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        # Tutti i loggati approvati possono leggere
        if request.method in permissions.SAFE_METHODS:
            return request.user.approvato
        # Solo admin e tecnico possono scrivere
        return request.user.ruolo in ['admin', 'tecnico']

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

class ComponenteViewSet(viewsets.ModelViewSet):
    queryset = Componente.objects.all()
    serializer_class = ComponenteSerializer
    permission_classes = [PermessoPerRuolo]