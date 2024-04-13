from rest_framework.routers import DefaultRouter

from .viewsets import AlimentViewSet

router = DefaultRouter()
router.register(r'aliment', AlimentViewSet)

urls = router.urls