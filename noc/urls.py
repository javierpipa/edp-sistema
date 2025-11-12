from rest_framework.routers import DefaultRouter
from .views import NoConformidadViewSet

router = DefaultRouter()
router.register(r'noc', NoConformidadViewSet)

urlpatterns = router.urls
