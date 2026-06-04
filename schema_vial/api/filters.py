from django_filters.rest_framework import DjangoFilterBackend

from .models import *
from .serializers import *
from .baseviewset import BaseViewSet

class EmpresaViewSet(BaseViewSet):

    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer

    filter_backends = [DjangoFilterBackend]

    filterset_fields = [
        'nombre',
        'activo'
    ]

class DocumentoViewSet(BaseViewSet):
    queryset = Documento.objects.all()
    serializer_class = DocumentoSerializer

    filter_backends = [DjangoFilterBackend]

    filterset_fields = [
        'tipo_documento',
        'activo'
    ]
class ConductorViewSet(BaseViewSet):
    queryset = Conductor.objects.all()
    serializer_class = ConductorSerializer

    filter_backends = [DjangoFilterBackend]

    filterset_fields = [
        'nombre',
        'apellido',
        'numero_documento',
        'activo'
    ]

class VehiculoViewSet(BaseViewSet):
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer

    filter_backends = [DjangoFilterBackend]

    filterset_fields = [
        'placa',
        'marca',
        'modelo',
        'capacidad',
        'activo'
    ]

class EstacionViewSet(BaseViewSet):
    queryset = Estacion.objects.all()
    serializer_class = EstacionSerializer

    filter_backends = [DjangoFilterBackend]

    filterset_fields = [
        'nombre',
        'ciudad',
        'direccion',
        'activo'
    ]

class RutaViewSet(BaseViewSet):
    queryset = Ruta.objects.all()
    serializer_class = RutaSerializer

    filter_backends = [DjangoFilterBackend]

    filterset_fields = [
        'origen',
        'destino',
        'nombre_ruta',
        'distancia_km',
        'activo'
    ]

class PasajeroViewSet(BaseViewSet):
    queryset = Pasajero.objects.all()
    serializer_class = PasajeroSerializer

    filter_backends = [DjangoFilterBackend]

    filterset_fields = [
        'nombre',
        'apellido',
        'numero_documento',
        'activo'
    ]

class ViajeViewSet(BaseViewSet):
    queryset = Viaje.objects.all()
    serializer_class = ViajeSerializer

    filter_backends = [DjangoFilterBackend]

    filterset_fields = [
        'vehiculo',
        'conductor',
        'ruta',
        'activo'
    ]

class BoletoViewSet(BaseViewSet):
    queryset = Boleto.objects.all()
    serializer_class = BoletoSerializer

    filter_backends = [DjangoFilterBackend]

    filterset_fields = [
        'viaje',
        'pasajero',
        'numero_asiento',
        'precio',
        'activo'
    ]

class MantenimientoViewSet(BaseViewSet):
    queryset = Mantenimiento.objects.all()
    serializer_class = MantenimientoSerializer

    filter_backends = [DjangoFilterBackend]

    filterset_fields = [
        'vehiculo',
        'activo'
    ]