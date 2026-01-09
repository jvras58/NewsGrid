"""
FastAPI Application Entry Point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.analyze.routes import router as analyze_router
from utils.settings import settings
from utils.logging import setup_logging

# Configurar logging
setup_logging()

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


app.include_router(analyze_router, prefix="/api/v1/analyze", tags=["Analyze"])


@app.get("/")
async def root():
    return {"message": "Agents API", "docs": "/docs", "version": settings.api_version}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=settings.api_host, port=settings.api_port)
