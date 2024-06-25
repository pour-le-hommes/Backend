from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List, Dict, Union
import os
from dotenv import load_dotenv

load_dotenv()



class TextClassification(BaseModel):
    passkey : str = os.getenv("passkey")
    prompt : str = "recommended that you keep it low to limit the payload size of accidental or malicious requests."


class ClassificationResponse(BaseModel):
    text: str
    classification: List[Dict[str, Union[str, float]]]

class SuccessfulClassification(BaseModel):
    response: ClassificationResponse

    class Config:
        json_schema_extra = {
            "example": {
                "response": {
                    "text": "recommended that you keep it low to limit the payload size of accidental or malicious requests.",
                    "classification": [
                        {'label': 'NEGATIVE', 'score': 0.9925075173377991}, 
                        {'label': 'POSITIVE', 'score': 0.007492518052458763}
                    ]
                }
            }
        }