import secrets
import string
from django.core.mail import send_mail
from rest_framework import generics, permissions, serializers as drf_serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Utente, LogAzione
from .serializers import UtenteSerializer, RegistrazioneSerializer


def registra_log(utente, azione):
    LogAzione.objects.create(utente=utente, azione=azione)


def genera_password_temporanea(lunghezza=12):
    chars = string.ascii_letters + string.digits
    return ''.join(secrets.choice(chars) for _ in range(lunghezza))


class RegistrazioneView(generics.CreateAPIView):
    serializer_class = RegistrazioneSerializer
    permission_classes = [permissions.AllowAny]


class ProfiloView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UtenteSerializer(request.user)
        return Response(serializer.data)


class ListaUtentiView(generics.ListAPIView):
    serializer_class = UtenteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.ruolo in ['admin', 'tecnico']:
            return Utente.objects.all()
        return Utente.objects.none()


class ApprovaUtenteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        if request.user.ruolo not in ['admin', 'tecnico']:
            return Response({'errore': 'Non autorizzato'}, status=403)
        try:
            utente = Utente.objects.get(pk=pk)

            password_temp = genera_password_temporanea()
            utente.set_password(password_temp)
            utente.approvato = True
            utente.save()

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
                from_email=None,
                recipient_list=[utente.email],
                fail_silently=False,
            )

            registra_log(request.user, f'Ha approvato l\'utente {utente.username}')

            return Response({'messaggio': f'{utente.username} approvato, email inviata a {utente.email}'})
        except Utente.DoesNotExist:
            return Response({'errore': 'Utente non trovato'}, status=404)


class LogSerializer(drf_serializers.ModelSerializer):
    utente = UtenteSerializer(read_only=True)

    class Meta:
        model = LogAzione
        fields = '__all__'


class LogView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if request.user.ruolo != 'admin':
            return Response({'errore': 'Non autorizzato'}, status=403)
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return LogAzione.objects.exclude(utente__ruolo='admin')