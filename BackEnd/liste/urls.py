from rest_framework.routers import DefaultRouter
from .views import ListaEsperienzaViewSet, ListaAcquistiViewSet

router = DefaultRouter()
router.register(r'esperienze', ListaEsperienzaViewSet, basename='esperienze')
router.register(r'acquisti', ListaAcquistiViewSet, basename='acquisti')

urlpatterns = router.urls