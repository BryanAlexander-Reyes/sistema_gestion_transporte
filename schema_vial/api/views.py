from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import *
from .baseviewset import BaseViewSet

# ViewSets
class EmpresaViewSet(BaseViewSet):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer

class ConductorViewSet(BaseViewSet):
    queryset = Conductor.objects.all()
    serializer_class = ConductorSerializer

class VehiculoViewSet(BaseViewSet):
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer

class EstacionViewSet(BaseViewSet):
    queryset = Estacion.objects.all()
    serializer_class = EstacionSerializer

class RutaViewSet(BaseViewSet):
    queryset = Ruta.objects.all()
    serializer_class = RutaSerializer

class DocumentoViewSet(BaseViewSet):
    queryset = Documento.objects.all()
    serializer_class = DocumentoSerializer

class PasajeroViewSet(BaseViewSet):
    queryset = Pasajero.objects.all()
    serializer_class = PasajeroSerializer

class ViajeViewSet(BaseViewSet):
    queryset = Viaje.objects.all()
    serializer_class = ViajeSerializer

class BoletoViewSet(BaseViewSet):
    queryset = Boleto.objects.all()
    serializer_class = BoletoSerializer

class MantenimientoViewSet(BaseViewSet):
    queryset = Mantenimiento.objects.all()
    serializer_class = MantenimientoSerializer
