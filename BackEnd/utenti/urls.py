from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegistrazioneView, ProfiloView, ListaUtentiView, ApprovaUtenteView

urlpatterns = [
    path('registrazione/', RegistrazioneView.as_view()),
    path('login/', TokenObtainPairView.as_view()),        # restituisce access + refresh token
    path('token/refresh/', TokenRefreshView.as_view()),   # rinnova l'access token
    path('profilo/', ProfiloView.as_view()),
    path('utenti/', ListaUtentiView.as_view()),
    path('utenti/<int:pk>/approva/', ApprovaUtenteView.as_view()),
]