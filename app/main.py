from app.presentation.routers import herramientas, prestamos, usuarios
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI(
    title="API Backend - Grupo 7",
    version="1.0.0",
    description="API REST acumulativa y persistente para el curso Desarrollo de Backend",
)

# Incluir los routers
app.include_router(usuarios.router)
app.include_router(herramientas.router)
app.include_router(prestamos.router)


# 1. Manejador para errores HTTP explícitos (404, 400, 403, etc.)
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "ok": False,
            "status_code": exc.status_code,
            "error": exc.detail,
            "path": request.url.path,
        },
    )


# 2. Manejador para errores de validación de Pydantic (422)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errores = []
    for err in exc.errors():
        campo = " -> ".join([str(loc) for loc in err["loc"]])
        errores.append({"campo": campo, "mensaje": err["msg"]})

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "ok": False,
            "status_code": 422,
            "error": "Error de validación en los datos enviados",
            "detalles": errores,
            "path": request.url.path,
        },
    )


# 3. Manejador de respaldo para errores no controlados del servidor (500)
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "ok": False,
            "status_code": 500,
            "error": "Error interno del servidor",
            "path": request.url.path,
        },
    )


@app.get("/")
def read_root():
    return {"mensaje": "API Backend operativa - Módulo de Miguel"}
