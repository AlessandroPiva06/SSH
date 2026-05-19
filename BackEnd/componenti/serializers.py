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
    tag = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        many=True, write_only=True,
        queryset=Tag.objects.all(), source='tag'
    )

    class Meta:
        model = Componente
        fields = '__all__'

    def validate_tag(self, value):
        if len(value) > 10:
            raise serializers.ValidationError("Puoi assegnare al massimo 10 tag per componente.")
        return value