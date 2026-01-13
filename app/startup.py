"""
FastAPI Application Entry Point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.api.analyze.routes import router as analyze_router
from app.api.auth.routes import router as auth_router
from app.api.user.routes import router as users_router
from utils.settings import settings
from utils.logging import setup_logging, get_logger
from scripts.seed_initial import seed_initial_user
from app.services.auth_service import AuthService

setup_logging()
logger = get_logger("startup")


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        users = AuthService.list_users()
    except Exception as e:
        logger.error(f"Falha ao listar usuários durante a inicialização.: {e}")
        raise
    if not users:
        try:
            seed_initial_user()
        except Exception as e:
            logger.error(f"Falha ao criar usuário inicial durante a inicialização: {e}")
            raise
    yield


app = FastAPI(
    title=settings.api_title,
    description="API para gerenciamento de agentes inteligentes.",
    version=settings.api_version,
    debug=settings.debug,
    docs_url=settings.docs_url,
    redoc_url=settings.redoc_url,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(users_router, prefix="/api/v1/users", tags=["Users"])
app.include_router(analyze_router, prefix="/api/v1/analyze", tags=["Analyze"])


@app.get("/")
async def root():
    return {"message": "Agents API", "docs": "/docs", "version": settings.api_version}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=settings.api_host, port=settings.api_port)
