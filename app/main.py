from fastapi import FastAPI

app = FastAPI(
    title="API Backend - Grupo 7",
    version="1.0.0",
    description="API REST acumulativa y persistente para el curso Desarrollo de Backend"
)

@app.get("/")
def read_root():
    return {"mensaje": "API Backend operativa - Módulo de Miguel"}
