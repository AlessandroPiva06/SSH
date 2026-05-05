from rest_framework import viewsets, permissions
from .models import Movimento
from .serializers import MovimentoSerializer

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