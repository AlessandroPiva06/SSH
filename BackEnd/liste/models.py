from django.db import models
from BackEnd.utenti.models import Utente
from BackEnd.componenti.models import Componente

class ListaEsperienza(models.Model):
    nome = models.CharField(max_length=200)
    professore = models.ForeignKey(Utente, on_delete=models.CASCADE)
    creata_il = models.DateTimeField(auto_now_add=True)
    componenti = models.ManyToManyField(Componente, through='VoceListaEsperienza')

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = "Liste esperienze"

class VoceListaEsperienza(models.Model):
    lista = models.ForeignKey(ListaEsperienza, on_delete=models.CASCADE)
    componente = models.ForeignKey(Componente, on_delete=models.CASCADE)
    quantita_necessaria = models.PositiveIntegerField(default=1)

class ListaAcquisti(models.Model):
    creata_il = models.DateTimeField(auto_now_add=True)
    creata_da = models.ForeignKey(Utente, on_delete=models.SET_NULL, null=True)
    componenti = models.ManyToManyField(Componente, through='VoceListaAcquisti')

    def __str__(self):
        return f"Lista acquisti del {self.creata_il:%d/%m/%Y}"

    class Meta:
        verbose_name_plural = "Liste acquisti"

class VoceListaAcquisti(models.Model):
    lista = models.ForeignKey(ListaAcquisti, on_delete=models.CASCADE)
    componente = models.ForeignKey(Componente, on_delete=models.CASCADE)
    quantita_da_acquistare = models.PositiveIntegerField(default=1)