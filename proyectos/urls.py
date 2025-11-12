from rest_framework.routers import DefaultRouter
from .views import ProyectoViewSet, CuadroControlViewSet

router = DefaultRouter()
router.register(r'proyectos', ProyectoViewSet)
router.register(r'controles', CuadroControlViewSet)

urlpatterns = router.urls
