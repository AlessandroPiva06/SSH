from rest_framework import serializers
from .models import Utente

class UtenteSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    vecchia_password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Utente
        fields = ['id', 'username', 'email', 'ruolo', 'approvato', 'password', 'vecchia_password']
        read_only_fields = ['ruolo', 'approvato']

    def update(self, instance, validated_data):
        vecchia = validated_data.pop('vecchia_password', None)
        nuova   = validated_data.pop('password', None)

        if nuova:
            if not vecchia:
                raise serializers.ValidationError({'vecchia_password': 'Inserisci la password attuale.'})
            if not instance.check_password(vecchia):
                raise serializers.ValidationError({'vecchia_password': 'Password attuale errata.'})
            instance.set_password(nuova)

        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        instance.save()
        return instance

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