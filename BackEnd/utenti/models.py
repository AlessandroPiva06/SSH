from django.contrib.auth.models import AbstractUser
from django.db import models

class Utente(AbstractUser):
    RUOLI = [
        ('admin', 'Amministratore'),
        ('tecnico', 'Tecnico'),
        ('professore', 'Professore'),
    ]
    ruolo = models.CharField(max_length=20, choices=RUOLI, default='professore')
    approvato = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username} ({self.ruolo})"

class LogAzione(models.Model):
    utente = models.ForeignKey(Utente, on_delete=models.SET_NULL, null=True)
    azione = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.timestamp:%d/%m/%Y %H:%M} — {self.utente} — {self.azione}"

    class Meta:
        verbose_name_plural = "Log azioni"
        ordering = ['-timestamp']