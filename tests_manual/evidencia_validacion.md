# Evidencia: errores de validación

Fecha: ____ / ____ / 2026   Ejecutado por: ______________

| ID | Qué se prueba | Petición | Esperado | Obtenido | ¿Cumple? |
|----|---------------|----------|----------|----------|----------|
| V1 | Campo obligatorio (email) | POST /usuarios/ sin email | 422 | 422 | si |
| V2 | Tipo (categoria_id texto) | POST /herramientas/ | 422 | 422 | si |
| V3 | Campo obligatorio (serial) | POST /herramientas/ sin serial | 422 | 422 | si |
| V4 | Tipo (usuario_id texto) | POST /prestamos/ | 422 | 422 | si |
| V5 | Formato de email | POST /usuarios/ email inválido | 422 | 422 | si |
| V6 | Longitud de nombre | POST /usuarios/ nombre vacío | 422 | 422 | si |


