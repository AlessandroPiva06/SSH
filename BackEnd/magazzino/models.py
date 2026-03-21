from django.db import models
from BackEnd.utenti.models import Utente
from BackEnd.componenti.models import Componente

class Movimento(models.Model):
    TIPI = [
        ('carico', 'Carico'),
        ('scarico', 'Scarico'),
    ]
    componente = models.ForeignKey(Componente, on_delete=models.CASCADE)
    utente = models.ForeignKey(Utente, on_delete=models.SET_NULL, null=True)
    tipo = models.CharField(max_length=10, choices=TIPI)
    quantita = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True)

    def __str__(self):
        return f"{self.tipo} {self.componente} x{self.quantita} — {self.timestamp:%d/%m/%Y %H:%M}"

    class Meta:
        verbose_name_plural = "Movimenti"