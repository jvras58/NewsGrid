"""
Schemas para requisições de análise.
"""

from pydantic import BaseModel


class AnalyzeRequestType(BaseModel):
    topic: str
