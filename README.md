# Sistema de Gestion de Transporte - API

Este proyecto es una API hecha con Django REST Framework para manejar la informacion principal de un sistema de transporte. La idea es poder administrar empresas, conductores, vehiculos, estaciones, rutas, pasajeros, viajes, boletos y mantenimientos.

La API tambien tiene varias mejoras que se fueron agregando durante el desarrollo, como autenticacion JWT, Swagger, paginacion, filtros, ordenamiento, soft delete, auditoria, logging, roles y permisos, nested serializers, exportacion a Excel y respuestas JSON personalizadas.

## Tecnologias usadas

- Python
- Django
- Django REST Framework
- PostgreSQL
- JWT con `djangorestframework-simplejwt`
- Swagger con `drf_yasg`
- Django Filters

## Estructura general

El proyecto principal esta dentro de la carpeta:

```text
schema_vial/
```

Archivos importantes:

```text
schema_vial/manage.py
schema_vial/run.py
schema_vial/backend/settings.py
schema_vial/backend/urls.py
schema_vial/api/models.py
schema_vial/api/serializers.py
schema_vial/api/views.py
schema_vial/api/urls.py
schema_vial/api/baseviewset.py
schema_vial/api/base_models.py
schema_vial/api/permissions.py
```

## Como ejecutar el proyecto

Primero se entra a la carpeta del proyecto:

```powershell
cd schema_vial
```

Luego se activa el entorno virtual:

```powershell
.\venv\Scripts\activate
```

Si hace falta instalar JWT:

```powershell
python -m pip install djangorestframework-simplejwt
```

Despues se ejecutan migraciones:

```powershell
python manage.py migrate
```

Y se corre el servidor:

```powershell
python run.py
```

Entonces la API queda en:

```text
http://127.0.0.1:8080/api/v1/
```

## Swagger

La documentacion visual de la API esta en:

```text
http://127.0.0.1:8080/swagger/
```

Desde Swagger se pueden ver los endpoints, probar peticiones, enviar parametros y revisar respuestas.

## Autenticacion JWT

La API tiene autenticacion con JWT.

Para pedir token:

```text
POST /api/v1/auth/token/
```

Ejemplo de body:

```json
{
  "username": "user",
  "password": "12345"
}
```

Respuesta esperada:

```json
{
  "refresh": "token_refresh",
  "access": "token_access"
}
```

Para usar el token en las peticiones protegidas:

```text
Authorization: Bearer TU_ACCESS_TOKEN
```

Tambien existen estas rutas:

```text
POST /api/v1/auth/token/refresh/
POST /api/v1/auth/token/verify/
```

## Endpoints principales

Todos los endpoints estan versionados con `/api/v1/`.

| Recurso | Endpoint |
| --- | --- |
| Empresa | `/api/v1/empresa/` |
| Documento | `/api/v1/documento/` |
| Conductor | `/api/v1/conductor/` |
| Vehiculo | `/api/v1/vehiculo/` |
| Estacion | `/api/v1/estacion/` |
| Ruta | `/api/v1/ruta/` |
| Pasajero | `/api/v1/pasajero/` |
| Viaje | `/api/v1/viaje/` |
| Boleto | `/api/v1/boleto/` |
| Mantenimiento | `/api/v1/mantenimiento/` |
| Auditoria | `/api/v1/auditoria-registro/` |
| Roles | `/api/v1/roles/` |
| Permisos | `/api/v1/permisos/` |

## Operaciones CRUD

Cada recurso principal permite estas operaciones:

```text
GET     consultar registros
POST    crear registros
PUT     actualizar registros completos
PATCH   actualizar parcialmente
DELETE  eliminar logicamente con soft delete
```

Ejemplo:

```text
GET /api/v1/conductor/
POST /api/v1/conductor/
PUT /api/v1/conductor/1/
DELETE /api/v1/conductor/1/
```

## Respuestas JSON personalizadas

Las respuestas se centralizan en `BaseViewSet`.

Ejemplo de respuesta correcta:

```json
{
  "success": true,
  "message": "Registro encontrado",
  "status_code": 200,
  "data": {}
}
```

Ejemplo de error:

```json
{
  "success": false,
  "message": "Error de validacion",
  "errors": {}
}
```

## Soft Delete

El proyecto no borra fisicamente los registros principales. Cuando se usa `DELETE`, el registro cambia:

```text
activo = False
```

Esto permite conservar la informacion en la base de datos.

Por defecto, la API muestra solo registros activos. Si se quiere consultar por estado:

```text
/api/v1/conductor/?activo=true
/api/v1/conductor/?activo=false
```

Tambien existe una accion para restaurar:

```text
POST /api/v1/conductor/1/restore/
```

## Auditoria de registros

La auditoria guarda las operaciones importantes realizadas en la API.

Registra datos como:

- modelo afectado
- id del registro
- accion realizada
- usuario
- metodo HTTP
- ruta
- datos anteriores
- datos nuevos
- fecha

Endpoint:

```text
/api/v1/auditoria-registro/
```

Ejemplos:

```text
/api/v1/auditoria-registro/?modelo=Conductor
/api/v1/auditoria-registro/?accion=UPDATE
/api/v1/auditoria-registro/?ordering=-fecha
```

## Logging de operaciones

El proyecto tiene logging para registrar operaciones de la API. Esto ayuda a revisar que acciones se hicieron y por que ruta.

El archivo de log esta en:

```text
schema_vial/api.log
```

Se registran operaciones como:

```text
CREATE
UPDATE
SOFT_DELETE
EXPORT_EXCEL
```

## Filtros

Los endpoints tienen filtros usando `django_filters`.

Ejemplos:

```text
/api/v1/conductor/?nombre=Carlos
/api/v1/conductor/?apellido=Perez
/api/v1/vehiculo/?placa=ABC123
/api/v1/pasajero/?numero_documento=123456
/api/v1/viaje/?activo=true
```

## Ordenamiento

Para ordenar se usa el parametro `ordering`.

Ejemplos:

```text
/api/v1/conductor/?ordering=nombre
/api/v1/conductor/?ordering=-nombre
/api/v1/vehiculo/?ordering=placa
/api/v1/empresa/?ordering=fecha_creacion
```

Importante: el ordenamiento va despues de `?`, no como parte de la ruta.

Correcto:

```text
/api/v1/conductor/?ordering=nombre
```

Incorrecto:

```text
/api/v1/conductor/ordering=nombre
```

## Paginacion

La API usa paginacion por defecto.

Ejemplo:

```text
/api/v1/conductor/?page=2
```

Esto ayuda cuando hay muchos registros, porque no carga todo de una sola vez.

## Exportacion de informacion a Excel

Cada recurso hereda una accion para exportar informacion en formato compatible con Excel.

Ejemplo:

```text
/api/v1/conductor/exportar-excel/
```

Tambien se puede combinar con filtros y ordenamiento:

```text
/api/v1/conductor/exportar-excel/?activo=true&ordering=nombre
```

La exportacion limpia saltos de linea dentro de los datos para evitar problemas en el archivo.

## Versionado

La API esta versionada con:

```text
/api/v1/
```

Esto sirve para que en el futuro se pueda crear otra version, por ejemplo `/api/v2/`, sin romper la version actual.

## Roles y permisos

Se agrego control de roles usando grupos de Django.

Roles pensados:

- Administrador
- Operador
- Auditor
- Consulta

Reglas generales:

- Administrador puede gestionar todo.
- Operador puede crear, editar, eliminar y restaurar registros normales.
- Auditor puede revisar auditoria.
- Consulta puede revisar informacion.

Endpoints:

```text
/api/v1/roles/
/api/v1/permisos/
```

## Nested Serializers

La API tiene relaciones anidadas para que al consultar registros se vea mas informacion sin tener que hacer tantas peticiones.

Ejemplo en conductor:

```json
{
  "id_conductor": 1,
  "empresa": 1,
  "empresa_detalle": {
    "id_empresa": 1,
    "nombre_empresa": "Empresa ejemplo"
  },
  "documento": 1,
  "documento_detalle": {
    "id_documento": 1,
    "tipo_documento": "Cedula"
  }
}
```

Para crear o actualizar se siguen enviando los IDs normales, como `empresa` y `documento`.

## Recursos del sistema

### Empresa

Guarda informacion de las empresas de transporte.

Campos principales:

- nombre_empresa
- descripcion
- direccion
- activo

### Documento

Guarda tipos de documento.

Campos principales:

- tipo_documento
- activo

### Conductor

Guarda informacion de los conductores.

Campos principales:

- empresa
- nombre
- apellido
- numero_documento
- documento
- telefono
- licencia
- activo

### Vehiculo

Guarda informacion de los vehiculos.

Campos principales:

- placa
- marca
- modelo
- capacidad
- activo

### Estacion

Guarda estaciones o terminales.

Campos principales:

- nombre
- ciudad
- direccion
- id_conductor
- activo

### Ruta

Guarda rutas entre estaciones.

Campos principales:

- origen
- destino
- nombre_ruta
- distancia_km
- activo

### Pasajero

Guarda informacion de pasajeros.

Campos principales:

- nombre
- apellido
- numero_documento
- documento
- telefono
- correo
- activo

### Viaje

Relaciona vehiculo, conductor y ruta con fecha de salida y llegada.

Campos principales:

- vehiculo
- conductor
- ruta
- fecha_salida
- fecha_llegada
- activo

### Boleto

Guarda la compra de un boleto por pasajero.

Campos principales:

- viaje
- pasajero
- numero_asiento
- precio
- fecha_compra
- activo

### Mantenimiento

Guarda mantenimientos de vehiculos.

Campos principales:

- vehiculo
- descripcion
- fecha_mantenimiento
- costo
- activo
