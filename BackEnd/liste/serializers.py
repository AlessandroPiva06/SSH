from rest_framework import serializers
from .models import ListaEsperienza, ListaAcquisti, VoceListaEsperienza, VoceListaAcquisti

class VoceListaEsperienzaSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoceListaEsperienza
        fields = '__all__'

class ListaEsperienzaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListaEsperienza
        fields = '__all__'

class VoceListaAcquistiSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoceListaAcquisti
        fields = '__all__'

class ListaAcquistiSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListaAcquisti
        fields = '__all__'