from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Utente
from .serializers import UtenteSerializer, RegistrazioneSerializer

# Registrazione — chiunque può farlo
class RegistrazioneView(generics.CreateAPIView):
    serializer_class = RegistrazioneSerializer
    permission_classes = [permissions.AllowAny]

# Profilo utente loggato
class ProfiloView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UtenteSerializer(request.user)
        return Response(serializer.data)

# Lista utenti — solo admin
class ListaUtentiView(generics.ListAPIView):
    serializer_class = UtenteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.ruolo in ['admin', 'tecnico']:
            return Utente.objects.all()
        return Utente.objects.none()

# Approva utente — solo admin o tecnico
class ApprovaUtenteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        if request.user.ruolo not in ['admin', 'tecnico']:
            return Response({'errore': 'Non autorizzato'}, status=403)
        try:
            utente = Utente.objects.get(pk=pk)
            utente.approvato = True
            utente.save()
            return Response({'messaggio': f'{utente.username} approvato'})
        except Utente.DoesNotExist:
            return Response({'errore': 'Utente non trovato'}, status=404)