# Registro de Cambios

Todos los cambios notables en este proyecto serán documentados en este archivo

## [1.1.0] - 2025-12-08

### Añadido
- **Arquitectura API REST**: La API ha sido completamente refactorizada para seguir los principios REST.
- **Manejo de Errores Unificado**: Todos los endpoints de la API ahora devuelven respuestas de error en JSON (`{"status": "error", "message": "..."}`) en lugar de redirecciones HTML.
- **Decoradores de Validación**: La lógica para verificaciones de existencia, nombres duplicados y seguridad de archivos se ha movido a decoradores reutilizables `@file_validations` y `@folder_validations`.
- **Códigos de Estado HTTP Estándar**:
  - `201 Created` para creación exitosa de archivos/carpetas.
  - `400 Bad Request` para entrada inválida usando cuerpos JSON.
  - `404 Not Found` para recursos faltantes.
  - `409 Conflict` para recursos duplicados.

### Cambiado
- **Renombrado de Recursos**: Se usa `PATCH` con un cuerpo JSON en lugar de pasar parámetros en la URL.
  - **Antes**: `PATCH /api/file/oldname.txt/newname.txt`
  - **Ahora**: `PATCH /api/file/oldname.txt` con cuerpo `{"name": "newname.txt"}`
- **Creación de Carpetas**: `POST` a `/api/folder/` ahora devuelve `201 Created`.

### Problemas Conocidos
- **Frontend No Funcional**: El frontend actual no es compatible con los cambios de la API REST v1.1 y requiere actualización.

### Ejemplos de Uso (v1.1)

#### Subir un Archivo
```bash
curl -X POST http://localhost/api/file/path/to/folder \
  -F "file=@localfile.txt"
```

#### Renombrar un Archivo
```bash
curl -X PATCH http://localhost/api/file/path/to/file.txt \
  -H "Content-Type: application/json" \
  -d '{"name": "newname.txt"}'
```

#### Crear un Directorio
```bash
curl -X POST http://localhost/api/folder/new_folder_path
```

#### Eliminar un Directorio
```bash
curl -X DELETE http://localhost/api/folder/folder_to_delete
```
