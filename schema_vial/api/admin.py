from django.contrib import admin
from .models import AuditoriaRegistro

# Register your models here.

# Auditoría de registros
@admin.register(AuditoriaRegistro)
class AuditoriaRegistroAdmin(admin.ModelAdmin):
    list_display = (
        'id_auditoria',
        'modelo',
        'registro_id',
        'accion',
        'usuario',
        'metodo',
        'fecha',
    )
    list_filter = ('modelo', 'accion', 'metodo', 'fecha')
    search_fields = ('modelo', 'registro_id', 'ruta')
    readonly_fields = (
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
