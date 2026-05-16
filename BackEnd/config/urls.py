from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('componenti.urls')),
    path('api/', include('magazzino.urls')),
    path('api/', include('liste.urls')),
    path('api/auth/', include('utenti.urls')),

    # Frontend
    path('', TemplateView.as_view(template_name='Home.html'), name='home'),
    path('login/', TemplateView.as_view(template_name='LogIn.html'), name='login'),
    path('registrazione/', TemplateView.as_view(template_name='Signin.html'), name='signin'),
    path('prodotto/', TemplateView.as_view(template_name='Product.html'), name='prodotto'),
]