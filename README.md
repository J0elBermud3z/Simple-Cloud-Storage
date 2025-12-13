<div align="center">

# Simple Cloud Storage  
![Status](https://img.shields.io/badge/Estado-En%20Desarrollo-yellow) ![Python](https://img.shields.io/badge/Python-3.10%2B-blue) ![Flask](https://img.shields.io/badge/Flask-2.x-green) ![Docker](https://img.shields.io/badge/Docker-Enabled-blue)

</div>

Una API de almacenamiento diseñada para crear tu propia nube privada en entornos locales. Construida con Flask, permite gestionar archivos y directorios de forma ágil, segura y flexible.

## Características (v1.1)

- **Gestión de Archivos**: Subir, descargar, renombrar y eliminar archivos.
- **Gestión de Carpetas**: Crear, listar, renombrar y eliminar directorios.
- **Diseño REST**: Métodos HTTP y códigos de estado estándar.
- **Dockerizado**: Fácil de desplegar y probar usando Docker.

## Comenzando

### Prerrequisitos

- Docker y Docker Compose
- *O* Python 3.10+ (para desarrollo local)

### Ejecutar con Docker

```bash
docker-compose up --build
```

La API estará disponible en `http://localhost`.

### Ejecutar Tests

Proveemos un Dockerfile para ejecutar las pruebas de forma aislada:

```bash
docker build -f backend/Dockerfile.test -t simple_cloud_tests backend

docker run --rm simple_cloud_tests
```

## Documentación de la API

Todos los endpoints de la API devuelven respuestas en JSON.

### URL Base: `/api`

### Archivos (`Files`)

| Método | Endpoint | Descripción | Cuerpo (Body) |
| :--- | :--- | :--- | :--- |
| `GET` | `/file/<path>` | Descargar metadatos/contenido del archivo | - |
| `POST` | `/file/<folder>` | Subir un archivo | `multipart/form-data`: `file` |
| `PATCH`| `/file/<path>` | Renombrar un archivo | `{"name": "new_name"}` |
| `DELETE`| `/file/<path>` | Eliminar un archivo | - |

### Carpetas (`Folders`)

| Método | Endpoint | Descripción | Cuerpo (Body) |
| :--- | :--- | :--- | :--- |
| `GET` | `/folder/<path>` | Listar contenido del directorio | - |
| `POST` | `/folder/<path>` | Crear un directorio | - |
| `PATCH`| `/folder/<path>` | Renombrar un directorio | `{"name": "new_name"}` |
| `DELETE`| `/folder/<path>` | Eliminar un directorio | - |

## Manejo de Errores

Los errores devuelven una estructura JSON genérica:

```json
{
  "status": "error",
  "message": "Descripción de qué salió mal"
}
```

Códigos de estado comunes:
- `400`: Solicitud Incorrecta (ej. JSON inválido, parámetros faltantes)
- `404`: No Encontrado
- `409`: Conflicto (ej. el nombre ya existe)
- `500`: Error Interno del Servidor
