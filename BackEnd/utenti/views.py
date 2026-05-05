from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Utente
from .serializers import UtenteSerializer, RegistrazioneSerializer
from django.core.mail import send_mail
import secrets, string
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
def genera_password_temporanea(lunghezza=12):
    chars = string.ascii_letters + string.digits
    return ''.join(secrets.choice(chars) for _ in range(lunghezza))

class ApprovaUtenteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        if request.user.ruolo not in ['admin', 'tecnico']:
            return Response({'errore': 'Non autorizzato'}, status=403)
        try:
            utente = Utente.objects.get(pk=pk)

            # Genera e imposta password temporanea
            password_temp = genera_password_temporanea()
            utente.set_password(password_temp)
            utente.approvato = True
            utente.save()

            # Manda email con credenziali
            send_mail(
                subject='Account approvato - Magazzino Fermi',
                message=(
                    f'Ciao {utente.username},\n\n'
                    f'Il tuo account è stato approvato.\n\n'
                    f'Le tue credenziali:\n'
                    f'Username: {utente.username}\n'
                    f'Password temporanea: {password_temp}\n\n'
                    f'Ti consigliamo di cambiare la password al primo accesso.\n\n'
                    f'Magazzino Fermi'
                ),
                from_email=None,  # usa DEFAULT_FROM_EMAIL
                recipient_list=[utente.email],
                fail_silently=False,
            )

            return Response({'messaggio': f'{utente.username} approvato, email inviata a {utente.email}'})
        except Utente.DoesNotExist:
            return Response({'errore': 'Utente non trovato'}, status=404)