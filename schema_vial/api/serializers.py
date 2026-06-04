from rest_framework import serializers
from django.contrib.auth.models import Group, Permission
from .models import *

class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = '__all__'
class DocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documento
        fields = '__all__'
class ConductorSerializer(serializers.ModelSerializer):
    # Relaciones anidadas (Nested Serializers)
    empresa_detalle = EmpresaSerializer(source='empresa', read_only=True)
    # Relaciones anidadas (Nested Serializers)
    documento_detalle = DocumentoSerializer(source='documento', read_only=True)

    class Meta:
        model = Conductor
        fields = '__all__'
class VehiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehiculo
        fields = '__all__'
class EstacionSerializer(serializers.ModelSerializer):
    # Relaciones anidadas (Nested Serializers)
    conductor_detalle = ConductorSerializer(source='id_conductor', read_only=True)

    class Meta:
        model = Estacion
        fields = '__all__'
class RutaSerializer(serializers.ModelSerializer):
    # Relaciones anidadas (Nested Serializers)
    origen_detalle = EstacionSerializer(source='origen', read_only=True)
    # Relaciones anidadas (Nested Serializers)
    destino_detalle = EstacionSerializer(source='destino', read_only=True)

    class Meta:
        model = Ruta
        fields = '__all__'
class PasajeroSerializer(serializers.ModelSerializer):
    # Relaciones anidadas (Nested Serializers)
    documento_detalle = DocumentoSerializer(source='documento', read_only=True)

    class Meta:
        model = Pasajero
        fields = '__all__'
class ViajeSerializer(serializers.ModelSerializer):
    # Relaciones anidadas (Nested Serializers)
    vehiculo_detalle = VehiculoSerializer(source='vehiculo', read_only=True)
    # Relaciones anidadas (Nested Serializers)
    conductor_detalle = ConductorSerializer(source='conductor', read_only=True)
    # Relaciones anidadas (Nested Serializers)
    ruta_detalle = RutaSerializer(source='ruta', read_only=True)

    class Meta:
        model = Viaje
        fields = '__all__'
class BoletoSerializer(serializers.ModelSerializer):
    # Relaciones anidadas (Nested Serializers)
    viaje_detalle = ViajeSerializer(source='viaje', read_only=True)
    # Relaciones anidadas (Nested Serializers)
    pasajero_detalle = PasajeroSerializer(source='pasajero', read_only=True)

    class Meta:
        model = Boleto
        fields = '__all__'
class MantenimientoSerializer(serializers.ModelSerializer):
    # Relaciones anidadas (Nested Serializers)
    vehiculo_detalle = VehiculoSerializer(source='vehiculo', read_only=True)

    class Meta:
        model = Mantenimiento
        fields = '__all__'

# Auditoría de registros
class AuditoriaRegistroSerializer(serializers.ModelSerializer):
    usuario_nombre = serializers.CharField(source='usuario.username', read_only=True)

    class Meta:
        model = AuditoriaRegistro
        fields = '__all__'
        read_only_fields = (
            'id_auditoria',
            'modelo',
            'registro_id',
            'accion',
            'usuario',
            'metodo',
            'ruta',
            'datos_anteriores',
            'datos_nuevos',
            'fecha',
        )

# Roles y permisos
class PermisoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = [
            'id',
            'name',
            'codename',
            'content_type',
        ]


# Roles y permisos
class RolSerializer(serializers.ModelSerializer):
    permissions = serializers.PrimaryKeyRelatedField(
        queryset=Permission.objects.all(),
        many=True,
        required=False
    )

    class Meta:
        model = Group
        fields = [
            'id',
            'name',
            'permissions',
        ]
