# Pruebas manuales (E2) - Grupo 7

Archivo: `api.http` (extensión **REST Client** de VS Code).

## Cómo ejecutarlas
1. `docker compose up --build`
2. Abrir `tests_manual/api.http`, presionar **Send Request** en cada bloque, de arriba hacia abajo.
3. Anotar el resultado obtenido en la tabla.

## Aislamiento de datos
Email, `codigo_serial` y similares llevan `{{$timestamp}}`: las pruebas se repiten sin choques.
Para partir de cero: `docker compose down -v` y luego `docker compose up --build`.

## Casos (esperado vs obtenido)

| ID | Tipo | Petición | Esperado | Obtenido |
|----|------|----------|----------|----------|
| 1.1 | Éxito | POST /usuarios/ | 201 | 201 |
| 1.3 | Éxito | GET /usuarios/ | 200 | 200 |
| 1.4 | Éxito | POST /herramientas/ | 201 | 201 |
| 1.6 | Éxito | GET /herramientas/{id} | 200 | 200 |
| 1.7 | Éxito | POST /prestamos/ | 201 | |
| 1.9 | Éxito | PUT /prestamos/{id}/devolver | 200 | 200 |
| 2.1 | Validación formato | POST /usuarios/ email inválido | 422 | 422 |
| 2.3 | Validación obligatorio | POST /herramientas/ sin serial | 422 | 422 |
| 3.1 | Inexistente | GET /herramientas/999999 | 404 | 404 |
| 3.5 | Duplicado | POST /usuarios/ email repetido | 409 | 409 |
| R1.b | Regla 1 | Prestar herramienta ya prestada | 400 | 400 |
| R2.b | Regla 2 | Devolver préstamo ya devuelto | 400 | 400 |
| R3.c | Regla 3 | 4.º préstamo activo del usuario | 400 | 400 |
| 5.1 | Filtro+orden+paginación | GET /herramientas/?categoria_id&ordenar_por&direccion&pagina&limite | 200 con metadatos | 200 |
| 6 | Persistencia | `down` + `up`, repetir 1.5 | mismos datos | 200 |

## Reglas de negocio
- **R1:** una herramienta con préstamo activo no puede prestarse otra vez.
- **R2:** un préstamo ya devuelto no puede devolverse de nuevo.
- **R3:** un usuario no puede tener más de 3 préstamos activos.

Errores controlados: `{"error": {"code": "...", "message": "...", "details": []}}`
