from django.db import models
from django.conf import settings
from .base_models import SoftDeleteModel

# modelo de empresa
class Empresa(SoftDeleteModel):
    id_empresa = models.AutoField(primary_key=True)
    nombre_empresa = models.CharField(max_length=100)
    descripcion = models.TextField()
    direccion = models.CharField(max_length=40)

    def __str__(self):
        return self.nombre_empresa

    class Meta:
        db_table = "empresa"


# modelo de documentos
class Documento(SoftDeleteModel):
    id_documento = models.AutoField(primary_key=True)
    tipo_documento = models.CharField(max_length=100)
    
    def __str__(self):
        return self.tipo_documento
    
    class Meta:
        db_table = "documento"

# Modelo de Conductores

class Conductor(SoftDeleteModel):
    id_conductor = models.AutoField(primary_key=True)
    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE
    )
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    numero_documento = models.CharField(max_length=200)
    documento = models.ForeignKey(Documento, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=20)
    licencia = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = "conductor"


# Modelo de Vehículos

class Vehiculo(SoftDeleteModel):
    id_vehiculo = models.AutoField(primary_key=True)
    placa = models.CharField(max_length=10)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    capacidad = models.IntegerField()


    def __str__(self):
        return self.placa

    class Meta:
        db_table = "vehiculo"


# Modelo de Estaciones

class Estacion(SoftDeleteModel):
    id_estacion = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    id_conductor = models.ForeignKey(
        Conductor,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = "estacion"


# Modelo de Rutas

class Ruta(SoftDeleteModel):
    id_ruta = models.AutoField(primary_key=True)

    origen = models.ForeignKey(
        Estacion,
        on_delete=models.CASCADE,
        related_name="rutas_origen"
    )

    destino = models.ForeignKey(
        Estacion,
        on_delete=models.CASCADE,
        related_name="rutas_destino"
    )

    nombre_ruta = models.CharField(max_length=100)
    distancia_km = models.DecimalField(max_digits=8, decimal_places=2)


    def __str__(self):
        return self.nombre_ruta

    class Meta:
        db_table = "ruta"



# Modelo de Pasajeros

class Pasajero(SoftDeleteModel):
    id_pasajero = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    numero_documento = models.CharField(max_length=200)
    documento = models.ForeignKey(Documento, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=20)
    correo = models.EmailField(unique=True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = "pasajero"


# Modelo de Viajes

class Viaje(SoftDeleteModel):
    id_viaje = models.AutoField(primary_key=True)

    vehiculo = models.ForeignKey(
        Vehiculo,
        on_delete=models.CASCADE
    )
    conductor = models.ForeignKey(
        Conductor,
        on_delete=models.CASCADE
    )
    ruta = models.ForeignKey(
        Ruta,
        on_delete=models.CASCADE
    )
    fecha_salida = models.DateTimeField()
    fecha_llegada = models.DateTimeField()

    def __str__(self):
        return f"Viaje {self.id_viaje}"

    class Meta:
        db_table = "viaje"


# Modelo de Boletos

class Boleto(SoftDeleteModel):
    id_boleto = models.AutoField(primary_key=True)
    viaje = models.ForeignKey(
        Viaje,
        on_delete=models.CASCADE
    )
    pasajero = models.ForeignKey(
        Pasajero,
        on_delete=models.CASCADE
    )
    numero_asiento = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_compra = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Boleto {self.id_boleto}"

    class Meta:
        db_table = "boleto"


# Modelo de Mantenimientos

class Mantenimiento(SoftDeleteModel):
    id_mantenimiento = models.AutoField(primary_key=True)
    vehiculo = models.ForeignKey(
        Vehiculo,
        on_delete=models.CASCADE
    )
    descripcion = models.TextField()
    fecha_mantenimiento = models.DateField()
    costo = models.DecimalField(max_digits=12, decimal_places=2)


    def __str__(self):
        return f"Mantenimiento {self.id_mantenimiento}"

    class Meta:
        db_table = "mantenimiento"


# Auditoría de registros
class AuditoriaRegistro(models.Model):
    id_auditoria = models.AutoField(primary_key=True)
    modelo = models.CharField(max_length=100)
    registro_id = models.CharField(max_length=100, blank=True, null=True)
    accion = models.CharField(max_length=50)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    metodo = models.CharField(max_length=10)
    ruta = models.CharField(max_length=255)
    datos_anteriores = models.JSONField(blank=True, null=True)
    datos_nuevos = models.JSONField(blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.accion} {self.modelo} {self.registro_id}"

    class Meta:
        db_table = "auditoria_registro"
        ordering = ["-fecha"]
