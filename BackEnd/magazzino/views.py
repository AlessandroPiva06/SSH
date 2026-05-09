from rest_framework import viewsets, permissions
from rest_framework.exceptions import ValidationError
from .models import Movimento
from .serializers import MovimentoSerializer
from componenti.models import Componente

class PermessoMagazzino(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.ruolo in ['admin', 'tecnico']

class MovimentoViewSet(viewsets.ModelViewSet):
    queryset = Movimento.objects.all().order_by('-timestamp')
    serializer_class = MovimentoSerializer
    permission_classes = [PermessoMagazzino]

    def perform_create(self, serializer):
        componente = serializer.validated_data['componente']
        tipo = serializer.validated_data['tipo']
        quantita = serializer.validated_data['quantita']

        if tipo == 'scarico':
            if componente.quantita < quantita:
                raise ValidationError(
                    f'Quantità insufficiente: disponibili {componente.quantita}, richiesti {quantita}.'
                )
            componente.quantita -= quantita
        else:
            componente.quantita += quantita

        componente.save()
        serializer.save(utente=self.request.user)