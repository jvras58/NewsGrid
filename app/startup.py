"""
FastAPI Application Entry Point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.analyze.routes import router as analyze_router
from app.api.auth.routes import router as auth_router
from app.api.status.routes import router as status_router
from app.api.user.routes import router as users_router
from utils.logging import get_logger, setup_logging
from utils.settings import settings

setup_logging()
logger = get_logger("startup")


app = FastAPI(
    title=settings.api_title,
    description="API para gerenciamento de agentes inteligentes.",
    version=settings.api_version,
    debug=settings.debug,
    docs_url=settings.docs_url,
    redoc_url=settings.redoc_url,
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
