from rest_framework import serializers
from .models import Componente, Famiglia, Tag, Locazione

class FamigliaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Famiglia
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class LocazioneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Locazione
        fields = '__all__'

class ComponenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Componente
        fields = '__all__'