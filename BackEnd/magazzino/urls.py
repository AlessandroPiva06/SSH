from rest_framework.routers import DefaultRouter
from .views import MovimentoViewSet

router = DefaultRouter()
router.register(r'movimenti', MovimentoViewSet)

urlpatterns = router.urls