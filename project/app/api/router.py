from rest_framework.routers import DefaultRouter

from .viewsets import AlimentViewSet, RetetaViewSet

router = DefaultRouter()
router.register(r'aliment', AlimentViewSet)
router.register(r'reteta', RetetaViewSet)

urls = router.urls