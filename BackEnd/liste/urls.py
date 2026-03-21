from rest_framework.routers import DefaultRouter
from .views import ListaEsperienzaViewSet, ListaAcquistiViewSet

router = DefaultRouter()
router.register(r'esperienze', ListaEsperienzaViewSet)
router.register(r'acquisti', ListaAcquistiViewSet)

urlpatterns = router.urls