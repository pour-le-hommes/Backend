from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class MemorizeInformation(BaseModel):
    info: str = Field(..., description="The semantic content of the memory.")
    memory_type: str = Field(..., description="Type of memory: e.g., 'preference', 'goal', 'trait'.")
    source: Optional[str] = Field(None, description="Origin of the memory: 'user', 'system', or 'inferred'.")
    confidence: Optional[float] = Field(None, ge=0.0, le=1.0, description="Confidence score between 0 and 1.")
    tags: List[str] = Field(default_factory=list, description="Tags for grouping or categorization.")
    embedding: Optional[List[float]] = Field(None, description="Vector representation of the memory content.")

class RecallInformation(BaseModel):
    info: str = Field(..., description="The semantic content of the memory.")
    top_k: int = Field(3, description="Amount of probability want to be taken account.")
    embedding: Optional[List[float]] = Field(None, description="Vector representation of the memory content.")