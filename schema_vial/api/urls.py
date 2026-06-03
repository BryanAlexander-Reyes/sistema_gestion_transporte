from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'empresa', EmpresaViewSet)
router.register(r'conductor', ConductorViewSet)
router.register(r'vehiculo', VehiculoViewSet)
router.register(r'estacion', EstacionViewSet)
router.register(r'ruta', RutaViewSet)
router.register(r'documento', DocumentoViewSet)
router.register(r'pasajero', PasajeroViewSet)
router.register(r'viaje', ViajeViewSet)
router.register(r'boleto', BoletoViewSet)
router.register(r'mantenimiento', MantenimientoViewSet)

urlpatterns = router.urls