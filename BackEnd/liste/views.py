from rest_framework import viewsets, permissions
from .models import ListaEsperienza, ListaAcquisti
from .serializers import ListaEsperienzaSerializer, ListaAcquistiSerializer

class ListaEsperienzaViewSet(viewsets.ModelViewSet):
    serializer_class = ListaEsperienzaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.ruolo in ['admin', 'tecnico']:
            return ListaEsperienza.objects.all()
        # Il professore vede solo le sue
        return ListaEsperienza.objects.filter(professore=user)

    def perform_create(self, serializer):
        # Il professore viene assegnato automaticamente
        serializer.save(professore=self.request.user)


class ListaAcquistiViewSet(viewsets.ModelViewSet):
    serializer_class = ListaAcquistiSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        # Solo admin e tecnico possono accedere
        if self.request.user.ruolo not in ['admin', 'tecnico']:
            self.permission_denied(self.request)
        return super().get_permissions()

    def get_queryset(self):
        return ListaAcquisti.objects.all()

    def perform_create(self, serializer):
        serializer.save(creata_da=self.request.user)