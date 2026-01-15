"""
FastAPI Application Entry Point
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.analyze.routes import router as analyze_router
from app.api.auth.routes import router as auth_router
from app.api.status.routes import router as status_router
from app.api.user.routes import router as users_router
from app.core.database import async_session
from app.services.auth_service_sql import AuthServiceSQL
from scripts.seed_initial import seed_initial_user
from utils.logging import get_logger, setup_logging
from utils.settings import settings

setup_logging()
logger = get_logger("startup")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # TODO: get_db aqui?
    async with async_session() as session:
        try:
            count = await AuthServiceSQL.count_users(session)
        except Exception as e:
            logger.error(f"Falha ao contar usuários durante a inicialização: {e}")
            raise
        if count == 0:
            try:
                await seed_initial_user()
            except Exception as e:
                logger.error(
                    f"Falha ao criar usuário inicial durante a inicialização: {e}"
                )
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
app.include_router(status_router, prefix="/api/v1/status", tags=["Status"])


@app.get("/")
async def root():
    return {"message": "Agents API", "docs": "/docs", "version": settings.api_version}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=settings.api_host, port=settings.api_port)
