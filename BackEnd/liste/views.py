import csv
from django.http import HttpResponse
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import ListaEsperienza, ListaAcquisti, VoceListaEsperienza, VoceListaAcquisti
from .serializers import ListaEsperienzaSerializer, ListaAcquistiSerializer, VoceListaEsperienzaSerializer, VoceListaAcquistiSerializer
from componenti.models import Componente


class ListaEsperienzaViewSet(viewsets.ModelViewSet):
    serializer_class = ListaEsperienzaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.ruolo in ['admin', 'tecnico']:
            return ListaEsperienza.objects.all()
        return ListaEsperienza.objects.filter(professore=user)

    def perform_create(self, serializer):
        serializer.save(professore=self.request.user)

    @action(detail=True, methods=['post'], url_path='aggiungi_componente')
    def aggiungi_componente(self, request, pk=None):
        lista = self.get_object()
        user = request.user

        if user.ruolo == 'professore' and lista.professore != user:
            return Response({'errore': 'Non autorizzato'}, status=403)

        componente_id = request.data.get('componente')
        quantita = request.data.get('quantita_necessaria', 1)

        if not componente_id:
            return Response({'errore': 'Componente mancante'}, status=400)

        try:
            componente = Componente.objects.get(pk=componente_id)
        except Componente.DoesNotExist:
            return Response({'errore': 'Componente non trovato'}, status=404)

        voce, created = VoceListaEsperienza.objects.update_or_create(
            lista=lista,
            componente=componente,
            defaults={'quantita_necessaria': quantita}
        )
        return Response(VoceListaEsperienzaSerializer(voce).data, status=201)

    @action(detail=True, methods=['delete'], url_path='rimuovi_componente/(?P<comp_id>[^/.]+)')
    def rimuovi_componente(self, request, pk=None, comp_id=None):
        lista = self.get_object()
        user = request.user

        if user.ruolo == 'professore' and lista.professore != user:
            return Response({'errore': 'Non autorizzato'}, status=403)

        VoceListaEsperienza.objects.filter(lista=lista, componente_id=comp_id).delete()
        return Response(status=204)


class PermessoAcquisti(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.ruolo in ['admin', 'tecnico']


class ListaAcquistiViewSet(viewsets.ModelViewSet):
    serializer_class = ListaAcquistiSerializer
    permission_classes = [PermessoAcquisti]

    def get_queryset(self):
        return ListaAcquisti.objects.all()

    def perform_create(self, serializer):
        serializer.save(creata_da=self.request.user)

    @action(detail=True, methods=['post'], url_path='aggiungi_componente')
    def aggiungi_componente(self, request, pk=None):
        lista = self.get_object()
        componente_id = request.data.get('componente')
        quantita = request.data.get('quantita_da_acquistare', 1)

        if not componente_id:
            return Response({'errore': 'Componente mancante'}, status=400)

        try:
            componente = Componente.objects.get(pk=componente_id)
        except Componente.DoesNotExist:
            return Response({'errore': 'Componente non trovato'}, status=404)

        voce, created = VoceListaAcquisti.objects.update_or_create(
            lista=lista,
            componente=componente,
            defaults={'quantita_da_acquistare': quantita}
        )
        return Response(VoceListaAcquistiSerializer(voce).data, status=201)

    @action(detail=True, methods=['delete'], url_path='rimuovi_componente/(?P<comp_id>[^/.]+)')
    def rimuovi_componente(self, request, pk=None, comp_id=None):
        lista = self.get_object()
        VoceListaAcquisti.objects.filter(lista=lista, componente_id=comp_id).delete()
        return Response(status=204)

    @action(detail=True, methods=['get'], url_path='esporta_csv')
    def esporta_csv(self, request, pk=None):
        lista = self.get_object()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="lista_acquisti_{lista.id}.csv"'

        writer = csv.writer(response)
        writer.writerow(['Componente', 'Quantità da acquistare'])
        for voce in lista.vocelistaacquisti_set.all():
            writer.writerow([voce.componente.nome, voce.quantita_da_acquistare])

        return response