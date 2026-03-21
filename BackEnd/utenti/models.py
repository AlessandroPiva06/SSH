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