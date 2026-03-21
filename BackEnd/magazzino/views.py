from rest_framework import viewsets
from .models import Movimento
from .serializers import MovimentoSerializer

class MovimentoViewSet(viewsets.ModelViewSet):
    queryset = Movimento.objects.all()
    serializer_class = MovimentoSerializer