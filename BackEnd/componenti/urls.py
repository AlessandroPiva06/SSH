from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import ComponenteViewSet, FamigliaViewSet, TagViewSet, LocazioneViewSet, product_page

router = DefaultRouter()
router.register(r'famiglie', FamigliaViewSet)
router.register(r'tag', TagViewSet)
router.register(r'locazioni', LocazioneViewSet)
router.register(r'componenti', ComponenteViewSet)

urlpatterns = router.urls + [
    path('product/', product_page, name='product-page'),
]