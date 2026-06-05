from django.shortcuts import render
from django.contrib.auth.models import Group, Permission
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
    # Relaciones anidadas (Nested Serializers)
    queryset = Conductor.objects.select_related('empresa', 'documento').all()
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
    # Relaciones anidadas (Nested Serializers)
    queryset = Estacion.objects.select_related(
        'id_conductor',
        'id_conductor__empresa',
        'id_conductor__documento'
    ).all()
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
    # Relaciones anidadas (Nested Serializers)
    queryset = Ruta.objects.select_related(
        'origen',
        'origen__id_conductor',
        'origen__id_conductor__empresa',
        'origen__id_conductor__documento',
        'destino',
        'destino__id_conductor',
        'destino__id_conductor__empresa',
        'destino__id_conductor__documento'
    ).all()
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
    # Relaciones anidadas (Nested Serializers)
    queryset = Pasajero.objects.select_related('documento').all()
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
    # Relaciones anidadas (Nested Serializers)
    queryset = Viaje.objects.select_related(
        'vehiculo',
        'conductor',
        'conductor__empresa',
        'conductor__documento',
        'ruta',
        'ruta__origen',
        'ruta__origen__id_conductor',
        'ruta__origen__id_conductor__empresa',
        'ruta__origen__id_conductor__documento',
        'ruta__destino',
        'ruta__destino__id_conductor',
        'ruta__destino__id_conductor__empresa',
        'ruta__destino__id_conductor__documento'
    ).all()
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
    # Relaciones anidadas (Nested Serializers)
    queryset = Boleto.objects.select_related(
        'viaje',
        'viaje__vehiculo',
        'viaje__conductor',
        'viaje__conductor__empresa',
        'viaje__conductor__documento',
        'viaje__ruta',
        'viaje__ruta__origen',
        'viaje__ruta__origen__id_conductor',
        'viaje__ruta__origen__id_conductor__empresa',
        'viaje__ruta__origen__id_conductor__documento',
        'viaje__ruta__destino',
        'viaje__ruta__destino__id_conductor',
        'viaje__ruta__destino__id_conductor__empresa',
        'viaje__ruta__destino__id_conductor__documento',
        'pasajero',
        'pasajero__documento'
    ).all()
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
    # Relaciones anidadas (Nested Serializers)
    queryset = Mantenimiento.objects.select_related('vehiculo').all()
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

# Roles y permisos
class RolViewSet(BaseViewSet):
    queryset = Group.objects.all()
    serializer_class = RolSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = [
        'name',
    ]
    ordering_fields = [
        'name',
    ]

# Roles y permisos
class PermisoViewSet(BaseViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermisoSerializer
    http_method_names = ['get', 'head', 'options']
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = [
        'codename',
        'content_type',
    ]
    ordering_fields = [
        'name',
        'codename',
    ]
