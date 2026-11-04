# Proyecto API REST - Gestión de Préstamos de Bodega (`backend-2026-grupo-07`)

API REST desarrollada con **FastAPI**, **SQLAlchemy** y **SQLite/PostgreSQL** para la gestión integral de inventario, herramientas, usuarios y préstamos de bodega.

## 📋 Tabla de Contenidos

* [Propósito del Proyecto](#-propósito-del-proyecto)
* [Tecnologías Utilizadas](#-tecnologías-utilizadas)
* [Arquitectura y Estructura del Proyecto](#-arquitectura-y-estructura-del-proyecto)
* [Flujo de una Solicitud entre Capas](#-flujo-de-una-solicitud-entre-capas)
* [Instalación y Configuración](#-instalación-y-configuración)
* [Base de Datos, Migraciones y Seeders](#-base-de-datos-migraciones-y-seeders)
* [Contrato OpenAPI y Endpoints](#-contrato-openapi-y-endpoints)
* [Reglas de Negocio y Validaciones](#-reglas-de-negocio-y-validaciones)
* [Evidencias de Casos de Prueba (SCRUM-28 a SCRUM-32)](#-evidencias-de-casos-de-prueba)
* [Integrantes y Responsabilidades](#-integrantes-y-responsabilidades)

## 🎯 Propósito del Proyecto

El sistema resuelve la problemática del control manual de inventario en bodegas técnicas o institucionales. Permite registrar usuarios, categorizar herramientas, controlar el stock unitario y gestionar préstamos, impidiendo duplicidades de uso y garantizando integridad transaccional.

## 🛠️ Tecnologías Utilizadas

* **Lenguaje:** Python 3.10+
* **Framework Web:** FastAPI
* **Servidor ASGI:** Uvicorn
* **ORM / Persistencia:** SQLAlchemy 2.0
* **Base de Datos:** SQLite (desarrollo/pruebas) / PostgreSQL compatible
* **Validación de Datos:** Pydantic v2
* **Migraciones:** Alembic

## 🏛️ Arquitectura y Estructura del Proyecto

El proyecto sigue una arquitectura organizada en **4 Capas de Responsabilidad** para garantizar un código modular, mantenible y escalable:

```
backend-2026-grupo-07/
├── app/
│   ├── main.py                     # Punto de entrada y ensamblaje de FastAPI
│   ├── presentation/               # Capa 1: Presentación (Endpoints y DTOs)
│   │   ├── dependencies.py         # Inyección de dependencias (Sesiones DB)
│   │   ├── routers/                # Enrutadores HTTP (usuarios, herramientas, etc.)
│   │   └── schemas/                # Schemas y DTOs Pydantic
│   ├── application/                # Capa 2: Aplicación (Casos de uso y Orquestación)
│   │   └── services/               # Servicios de lógica de aplicación
│   ├── domain/                     # Capa 3: Dominio (Entidades y Reglas de Negocio)
│   │   └── models/                 # Modelos de negocio e interfaces
│   └── infrastructure/             # Capa 4: Infraestructura (Persistencia y Datos)
│       ├── database.py             # Configuración del motor y sesión SQLAlchemy
│       ├── models/                 # Modelos ORM (SQLAlchemy)
│       ├── repositories/           # Repositorios de acceso a datos
│       └── seeders/                # Carga de datos iniciales
├── migrations/                     # Archivos de migración de Alembic
├── alembic.ini                     # Configuración de Alembic
├── .env.example                    # Plantilla de variables de entorno (sin secretos)
├── requirements.txt                # Dependencias del proyecto
└── README.md                       # Documentación técnica
```

## 🔄 Flujo de una Solicitud entre Capas

1. **Presentation Layer (Router):** Recibe la petición HTTP, procesa los parámetros query/path y valida la entrada con **Pydantic Schemas (DTOs)**.
2. **Application Layer (Service):** Coordina los casos de uso e invoca las validaciones del dominio.
3. **Domain Layer (Business Rules):** Ejecuta la lógica de negocio (ej. verificar que una herramienta no tenga un préstamo activo).
4. **Infrastructure Layer (Repository / Database):** Interactúa con la base de datos a través de **SQLAlchemy ORM** y retorna los resultados mapeados.
5. **Respuesta HTTP:** El Router convierte el modelo devuelto a un DTO de respuesta y retorna el código de estado correspondiente (`200`, `201`, `400`, `404`, `422`).

## ⚙️ Instalación y Configuración

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/backend-2026-grupo-07.git
cd backend-2026-grupo-07
```

### 2. Crear y activar un entorno virtual

```bash
# Linux/macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Copia la plantilla `.env.example` y renómbrala a `.env`:

```bash
cp .env.example .env
```

Ejemplo de contenido de `.env`:

```env
DATABASE_URL=sqlite:///./sql_app.db
APP_ENV=development
```

## 🗄️ Base de Datos, Migraciones y Seeders

### Ejecutar Migraciones (Alembic)

Para crear las tablas desde cero en la base de datos:

```bash
alembic upgrade head
```

### Ejecutar Seeders (Carga Inicial)

Para cargar datos iniciales de prueba (al menos 2 registros por entidad):

```bash
python -m app.infrastructure.seeders.seed_data
```

## 🚀 Ejecución de la API

Inicia el servidor local de desarrollo:

```bash
uvicorn app.main:app --reload
```

El servidor estará accesible en: `http://127.0.0.1:8000`

## 📜 Contrato OpenAPI y Endpoints

La documentación interactiva OpenAPI/Swagger se genera automáticamente y está disponible en:

* **Swagger UI:** `http://127.0.0.1:8000/docs`
* **ReDoc:** `http://127.0.0.1:8000/redoc`

### Resumen de Endpoints (12 Métodos Implementados)

| Entidad | Método | Ruta | Descripción |
| ----- | ----- | ----- | ----- |
| **Usuarios** | `POST` | `/usuarios/` | Crear un nuevo usuario |
| **Usuarios** | `GET` | `/usuarios/` | Listar todos los usuarios |
| **Usuarios** | `GET` | `/usuarios/{id}` | Obtener usuario por ID |
| **Categorías** | `POST` | `/categorias/` | Crear una nueva categoría |
| **Categorías** | `GET` | `/categorias/` | Listar todas las categorías |
| **Herramientas** | `POST` | `/herramientas/` | Crear una nueva herramienta |
| **Herramientas** | `GET` | `/herramientas/` | **Listar herramientas (con filtro, orden y paginación)** |
| **Herramientas** | `GET` | `/herramientas/{id}` | Obtener herramienta por ID |
| **Herramientas** | `PUT` | `/herramientas/{id}` | Actualizar datos de una herramienta |
| **Herramientas** | `DELETE` | `/herramientas/{id}` | Eliminar una herramienta |
| **Préstamos** | `POST` | `/prestamos/` | Registrar préstamo (Aplica Regla de Negocio) |
| **Préstamos** | `PUT` | `/prestamos/{id}/devolver` | Registrar devolución de herramienta |

## 🔐 Reglas de Negocio y Validaciones

1. **Unicidad de Usuario:** No se permite registrar usuarios con correos duplicados (`IntegrityError` redirigido a `400 Bad Request`).
2. **Existencia Relacionada:** Antes de crear un préstamo, se verifica la existencia previa del `usuario_id` y `herramienta_id`.
3. **Disponibilidad de Herramienta:** Una herramienta no se puede prestar si ya cuenta con un préstamo en estado `"activo"`. Si se intenta, la API retorna un error controlado `400 Bad Request`.
4. **Filtrado, Ordenamiento y Paginación Avanzada:** El endpoint `GET /herramientas/` permite combinar búsqueda de texto (`search`), filtrado por categoría (`categoria_id`), ordenación por campos (`sort_by`, `order`) y bloques de paginación (`skip`, `limit`).

## 🧪 Evidencias de Casos de Prueba (SCRUM-28 a SCRUM-32)

### 1. Colección de Endpoints (SCRUM-28)
* Endpoints documentados y probados directamente desde Swagger UI (`/docs`).

### 2. CRUD Completo Exitoso (SCRUM-29)
* **POST `/prestamos/`**
  * **Input:** `{"herramienta_id": 3, "usuario_id": 1}`
  * **Output (`201 Created`):** `{"id": 3, "herramienta_id": 3, "usuario_id": 1, "estado": "activo"}`

### 3. Error de Validación y Regla de Negocio (SCRUM-30)
* Intentar prestar la herramienta 3 estando activa.
  * **Output (`400 Bad Request`):**
    ```json
    {
      "ok": false,
      "status_code": 400,
      "error": "La herramienta ya se encuentra en préstamo activo.",
      "path": "/prestamos/"
    }
    ```

### 4. Filtrado, Ordenamiento y Paginación (SCRUM-31)
* **GET `/herramientas/?search=taladro&sort_by=nombre&order=asc&skip=0&limit=5`**
  * **Output (`200 OK`):** Retorna colección filtrada, ordenada alfabéticamente y paginada.

### 5. Persistencia Transaccional (SCRUM-32)
* Los datos insertados sobreviven al reinicio de la aplicación y la integridad referencial se mantiene ante errores transaccionales (rollback automático).

## 👥 Integrantes y Responsabilidades

| Estudiante | Área de Responsabilidad Principal | Tareas y Componentes a Cargo |
| :--- | :--- | :--- |
| **Miguel Obando** | API y Lógica de Negocio / Coordinación | Implementación de routers HTTP (`FastAPI`), servicios de aplicación, orquestación de capas y lógica de validación de reglas de negocio. |
| **Matías Queupumil** | Dominio y Datos / Infraestructura | Modelado de entidades relacionales (`Usuario`, `Categoria`, `Herramienta`, `Prestamo`), configuración de `SQLAlchemy` ORM, migraciones `Alembic` y seeders de carga inicial. |
| **Omar Grimaldy** | Calidad y Pruebas / Documentación e Integración | Gestión del backlog en Jira, ejecución y documentación de los 6 casos de prueba (`SCRUM-28` a `SCRUM-32`), integración de especificación OpenAPI y redacción técnica del README. |
