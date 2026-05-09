from rest_framework import serializers
from .models import Utente

class UtenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utente
        fields = ['id', 'username', 'email', 'ruolo', 'approvato']

class RegistrazioneSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Utente
        fields = ['username', 'email', 'password', 'ruolo']

    def create(self, validated_data):
        ruolo = validated_data.get('ruolo', 'professore')
        utente = Utente.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            ruolo=ruolo,
            approvato=False,
            is_staff=ruolo in ['admin', 'tecnico']
        )
        return utente