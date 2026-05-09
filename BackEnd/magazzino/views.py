from rest_framework import viewsets, permissions
from .models import Movimento
from .serializers import MovimentoSerializer
from utenti.views import registra_log

class PermessoMagazzino(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        # Solo admin e tecnico possono fare carico/scarico
        return request.user.ruolo in ['admin', 'tecnico']

class MovimentoViewSet(viewsets.ModelViewSet):
    queryset = Movimento.objects.all()
    serializer_class = MovimentoSerializer
    permission_classes = [PermessoMagazzino]

    def perform_create(self, serializer):
        obj = serializer.save()
        registra_log(self.request.user, f'Ha registrato un {obj.tipo} di {obj.quantita} pz per "{obj.componente}"')