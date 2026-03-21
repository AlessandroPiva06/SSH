from django.db import models

class Famiglia(models.Model):
    nome = models.CharField(max_length=100)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE,
        null=True, blank=True, related_name='figli'
    )
    class Meta:
        verbose_name_plural = "Famiglie"

    def __str__(self):
        return self.nome

class Tag(models.Model):
    nome = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = "Tag"


class Locazione(models.Model):
    ambiente = models.CharField(max_length=50)
    sezione = models.CharField(max_length=50)
    cassetto = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.ambiente} / {self.sezione} / {self.cassetto}"

    class Meta:
        verbose_name_plural = "Locazioni"


class Componente(models.Model):
    nome = models.CharField(max_length=200)
    famiglia = models.ForeignKey(Famiglia, on_delete=models.SET_NULL, null=True)
    tag = models.ManyToManyField(Tag, blank=True)
    locazione = models.ForeignKey(Locazione, on_delete=models.SET_NULL, null=True)
    link_datasheet = models.URLField(blank=True)
    quantita = models.PositiveIntegerField(default=0)
    quantita_minima = models.PositiveIntegerField(default=0)
    is_scorta = models.BooleanField(default=False)

    def __str__(self):
        return self.nome

    def sotto_scorta(self):
        return self.quantita <= self.quantita_minima

    class Meta:
        verbose_name_plural = "Componenti"