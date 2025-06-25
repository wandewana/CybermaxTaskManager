from fastapi import FastAPI
from app.api.router import api_router

app = FastAPI()

# Run Alembic migrations at startup
from app.alembic_runner import run_migrations

@app.on_event("startup")
def apply_migrations():
    run_migrations()

app.include_router(api_router)

@app.get("/")
def read_root():
    return {"message": "Server is running"}
