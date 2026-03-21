from rest_framework.routers import DefaultRouter
from .views import ComponenteViewSet, FamigliaViewSet, TagViewSet, LocazioneViewSet

router = DefaultRouter()
router.register(r'famiglie', FamigliaViewSet)
router.register(r'tag', TagViewSet)
router.register(r'locazioni', LocazioneViewSet)
router.register(r'componenti', ComponenteViewSet)

urlpatterns = router.urls