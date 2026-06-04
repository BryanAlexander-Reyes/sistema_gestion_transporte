from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import *
from .baseviewset import BaseViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter


# ViewSets
class EmpresaViewSet(BaseViewSet):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = [
        'nombre_empresa',
        'activo'
    ]
    ordering_fields = [
        'nombre_empresa',
        'fecha_creacion',
    ]

class ConductorViewSet(BaseViewSet):
    queryset = Conductor.objects.all()
    serializer_class = ConductorSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = [
        'nombre',
        'apellido',
        'numero_documento',
        'activo'
    ]
    ordering_fields = [
        'nombre',
        'apellido',
        'numero_documento',
        'fecha_creacion',
    ]
class VehiculoViewSet(BaseViewSet):
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = [
        'placa',
        'marca',
        'modelo',
        'capacidad',
        'activo'
    ]
    ordering_fields = [
        'placa',
        'marca',
        'modelo',
        'capacidad',
        'fecha_creacion',
    ]
class EstacionViewSet(BaseViewSet):
    queryset = Estacion.objects.all()
    serializer_class = EstacionSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = [
        'nombre',
        'ciudad',
        'direccion',
        'activo'
    ]
    ordering_fields = [
        'nombre',
        'ciudad',
        'direccion',
        'fecha_creacion',
    ]
class RutaViewSet(BaseViewSet):
    queryset = Ruta.objects.all()
    serializer_class = RutaSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = [
        'origen',
        'destino',
        'nombre_ruta',
        'distancia_km',
        'activo'
    ]
    ordering_fields = [
        'origen',
        'destino',
        'fecha_creacion',
    ]
class DocumentoViewSet(BaseViewSet):
    queryset = Documento.objects.all()
    serializer_class = DocumentoSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = [
        'tipo_documento',
        'activo'
    ]
    ordering_fields = [
        'tipo_documento',
        'fecha_creacion',
    ]
class PasajeroViewSet(BaseViewSet):
    queryset = Pasajero.objects.all()
    serializer_class = PasajeroSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = [
        'nombre',
        'apellido',
        'numero_documento',
        'activo'
    ]
    ordering_fields = [
        'nombre',
        'apellido',
        'numero_documento',
        'activo',
        'fecha_creacion',
    ]
class ViajeViewSet(BaseViewSet):
    queryset = Viaje.objects.all()
    serializer_class = ViajeSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = [
        'vehiculo',
        'conductor',
        'ruta',
        'activo'
    ]
    ordering_fields = [
        'vehiculo',
        'conductor',
        'ruta',
        'activo',
        'fecha_creacion',
    ]
class BoletoViewSet(BaseViewSet):
    queryset = Boleto.objects.all()
    serializer_class = BoletoSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = [
        'viaje',
        'pasajero',
        'numero_asiento',
        'precio',
        'activo'
    ]
    ordering_fields = [
        'viaje',
        'pasajero',
        'numero_asiento',
        'precio',
        'activo',
        'fecha_creacion',
    ]
class MantenimientoViewSet(BaseViewSet):
    queryset = Mantenimiento.objects.all()
    serializer_class = MantenimientoSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = [
        'vehiculo',
        'activo'
    ]
    ordering_fields = [
        'vehiculo',
        'activo',
        'fecha_creacion',
    ]

# Auditoría de registros
class AuditoriaRegistroViewSet(BaseViewSet):
    queryset = AuditoriaRegistro.objects.all()
    serializer_class = AuditoriaRegistroSerializer
    http_method_names = ['get', 'head', 'options']
    audit_enabled = False
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = [
        'modelo',
        'registro_id',
        'accion',
        'usuario',
        'metodo',
    ]
    ordering_fields = [
        'fecha',
        'modelo',
        'accion',
    ]
