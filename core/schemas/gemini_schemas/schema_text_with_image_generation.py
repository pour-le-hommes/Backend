from pydantic import BaseModel
import os
from typing import List, Dict

class TextImageGeneration(BaseModel):
    passkey : str = os.getenv("passkey","None")
    messages : List[Dict[str, any]] = [ # type: ignore
            {"role":"user", "content":"Can you help me?"},
            {"role":"assistant", "content":"Hello, of course. How can I help you?"},
            {"role":"user", "content":"Please explain Python to me"},
        ]

class SuccessfulTextImageGeneration(BaseModel):
    response: str

    class Config:
        json_schema_extra = {
            "example": {
                "response": "Of course, here's what I know regarding Python"
            }
        }