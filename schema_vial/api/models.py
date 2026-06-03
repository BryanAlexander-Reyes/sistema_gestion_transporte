from django.db import models

from django.db import models

# modelo de empresa
class Empresa(models.Model):
    id_empresa = models.AutoField(primary_key=True)
    nombre_empresa = models.CharField(max_length=100)
    descripcion = models.TextField()
    direccion = models.CharField(max_length=40)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre_empresa

    class Meta:
        db_table = "empresa"


# modelo de documentos
class Documento(models.Model):
    id_documento = models.AutoField(primary_key=True)
    tipo_documento = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)    
    
    def __str__(self):
        return self.tipo_documento
    
    class Meta:
        db_table = "documento"

# Modelo de Conductores

class Conductor(models.Model):
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
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = "conductor"


# Modelo de Vehículos

class Vehiculo(models.Model):
    id_vehiculo = models.AutoField(primary_key=True)
    placa = models.CharField(max_length=10)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    capacidad = models.IntegerField()

    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.placa

    class Meta:
        db_table = "vehiculo"


# Modelo de Estaciones

class Estacion(models.Model):
    id_estacion = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    id_conductor = models.ForeignKey(
        Conductor,
        on_delete=models.CASCADE,
    )
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = "estacion"


# Modelo de Rutas

class Ruta(models.Model):
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

    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre_ruta

    class Meta:
        db_table = "ruta"



# Modelo de Pasajeros

class Pasajero(models.Model):
    id_pasajero = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    numero_documento = models.CharField(max_length=200)
    documento = models.ForeignKey(Documento, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=20)
    correo = models.EmailField(unique=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = "pasajero"


# Modelo de Viajes

class Viaje(models.Model):
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
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Viaje {self.id_viaje}"

    class Meta:
        db_table = "viaje"


# Modelo de Boletos

class Boleto(models.Model):
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
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Boleto {self.id_boleto}"

    class Meta:
        db_table = "boleto"


# Modelo de Mantenimientos

class Mantenimiento(models.Model):
    id_mantenimiento = models.AutoField(primary_key=True)
    vehiculo = models.ForeignKey(
        Vehiculo,
        on_delete=models.CASCADE
    )
    descripcion = models.TextField()
    fecha_mantenimiento = models.DateField()
    costo = models.DecimalField(max_digits=12, decimal_places=2)

    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Mantenimiento {self.id_mantenimiento}"

    class Meta:
        db_table = "mantenimiento"