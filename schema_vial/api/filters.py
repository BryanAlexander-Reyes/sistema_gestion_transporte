from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

class ConductorViewSet(BaseViewSet):
    queryset = Conductor.objects.all().order_by('nombre')
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