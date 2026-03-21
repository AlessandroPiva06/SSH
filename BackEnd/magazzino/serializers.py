from rest_framework import serializers
from .models import Movimento

class MovimentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movimento
        fields = '__all__'