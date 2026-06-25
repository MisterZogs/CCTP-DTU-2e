import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.db.database import init_db
from src.rag.indexer import index_knowledge_base
from src.api.routes import projects, cctp, export


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    count = index_knowledge_base()
    print(f"Base de connaissances DTU : {count} chunks indexés")
    yield


app = FastAPI(
    title="CCTP Generator API",
    description="Générateur de CCTP IA avec base DTU — Claude & Mistral",
    version="0.1.0",
    lifespan=lifespan,
)

_origins_env = os.environ.get("ALLOWED_ORIGINS", "")
_allowed_origins = [o.strip() for o in _origins_env.split(",") if o.strip()] or ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(projects.router, prefix="/api/v1")
app.include_router(cctp.router, prefix="/api/v1")
app.include_router(export.router, prefix="/api/v1")


@app.get("/health")
async def health():
    return {"status": "ok"}
