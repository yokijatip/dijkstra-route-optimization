import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import benchmarks, datasets, routes
from app.services.firebase_service import get_firestore_status

app = FastAPI(
    title="Dijkstra Route Optimization API",
    description="Backend simulasi navigasi dan laboratorium benchmark Dijkstra.",
    version="0.1.0",
)

allowed_origins = [
    origin.strip()
    for origin in os.getenv(
        "ALLOWED_ORIGINS",
        "http://localhost:3000,http://127.0.0.1:3000,"
        "https://dijkstra-route-optimization.web.app,"
        "https://dijkstra-route-optimization.firebaseapp.com",
    ).split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health", tags=["system"])
def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "dijkstra-backend",
        "message": "Dijkstra Route Optimization API is running.",
    }


@app.get("/api/firebase/status", tags=["system"])
def firebase_status() -> dict[str, str | bool]:
    return get_firestore_status()


app.include_router(datasets.router)
app.include_router(routes.router)
app.include_router(benchmarks.router)
