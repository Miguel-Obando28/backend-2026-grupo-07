# Evidencia: CRUD completo de Herramienta

Fecha de ejecución: ____ / ____ / 2026   Ejecutado por: ______________

| Paso | Operación | Petición | Esperado | Obtenido | ¿Cumple? |
|------|-----------|----------|----------|----------|----------|
| C1 | Crear | POST /herramientas/ | 201 | 201 | si |
| C2 | Listar | GET /herramientas/ | 200, incluye la nueva | 200 | si |
| C3 | Obtener por ID | GET /herramientas/{id} | 200 | 200 | si |
| C4 | Actualizar | PUT /herramientas/{id} | 200 | 200 | si |
| C5 | Verificar cambio | GET /herramientas/{id} | 200, nombre actualizado | 200 | si |
| C6 | Eliminar | DELETE /herramientas/{id} | 204 | 204 | si |
| C7 | Verificar borrado | GET /herramientas/{id} | 404 | 404 | si |
| P | Persistencia | `down` + `up`, repetir C3 | mismo dato | 200 | si |
