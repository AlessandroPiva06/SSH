from rest_framework import serializers
from .models import ListaEsperienza, ListaAcquisti, VoceListaEsperienza, VoceListaAcquisti

class VoceListaEsperienzaSerializer(serializers.ModelSerializer):
    componente_nome = serializers.CharField(source='componente.nome', read_only=True)
    componente_quantita = serializers.IntegerField(source='componente.quantita', read_only=True)

    class Meta:
        model = VoceListaEsperienza
        fields = ['id', 'componente', 'componente_nome', 'componente_quantita', 'quantita_necessaria']

class ListaEsperienzaSerializer(serializers.ModelSerializer):
    voci = VoceListaEsperienzaSerializer(source='vocelistaesperienza_set', many=True, read_only=True)

    class Meta:
        model = ListaEsperienza
        fields = '__all__'

class VoceListaAcquistiSerializer(serializers.ModelSerializer):
    componente_nome = serializers.CharField(source='componente.nome', read_only=True)

    class Meta:
        model = VoceListaAcquisti
        fields = ['id', 'componente', 'componente_nome', 'quantita_da_acquistare']

class ListaAcquistiSerializer(serializers.ModelSerializer):
    voci = VoceListaAcquistiSerializer(source='vocelistaacquisti_set', many=True, read_only=True)
    creata_da_username = serializers.CharField(source='creata_da.username', read_only=True)

    class Meta:
        model = ListaAcquisti
        fields = '__all__'