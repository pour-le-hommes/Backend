from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List, Dict
import os
from dotenv import load_dotenv

load_dotenv()


class TextGeneration(BaseModel):
    passkey : str = os.getenv("passkey")
    messages : List[Dict[str, str]] = [
            {"role":"user", "content":"Can you help me?"},
            {"role":"assistant", "content":"Hello, of course. How can I help you?"},
            {"role":"user", "content":"Please explain Python to me"},
        ]

class SuccessfulGeneration(BaseModel):
    response: str

    class Config:
        json_schema_extra = {
            "example": {
                "response": "Of course, here's what I know regarding Python"
            }
        }