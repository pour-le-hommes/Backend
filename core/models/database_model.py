from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

class Memory(BaseModel):
    content: str = Field(..., description="The semantic content of the memory.")
    memory_type: str = Field(..., description="Type of memory: e.g., 'preference', 'goal', 'trait'.")
    source: Optional[str] = Field(None, description="Origin of the memory: 'user', 'system', or 'inferred'.")
    confidence: Optional[float] = Field(None, ge=0.0, le=1.0, description="Confidence score between 0 and 1.")
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow, description="Timestamp of creation.")
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow, description="Timestamp of last update.")
    tags: List[str] = Field(default_factory=list, description="Tags for grouping or categorization.")
    is_active: Optional[bool] = Field(default=True, description="Whether the memory is active.")
    embedding: Optional[List[float]] = Field(None, description="Vector representation of the memory content.")
