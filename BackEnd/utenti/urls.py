from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegistrazioneView, ProfiloView, ListaUtentiView, ApprovaUtenteView, LogView

urlpatterns = [
    path('registrazione/', RegistrazioneView.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('profilo/', ProfiloView.as_view()),
    path('utenti/', ListaUtentiView.as_view()),
    path('utenti/<int:pk>/approva/', ApprovaUtenteView.as_view()),
    path('log/', LogView.as_view()),
]