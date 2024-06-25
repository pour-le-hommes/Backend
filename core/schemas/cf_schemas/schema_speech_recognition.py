from fastapi import File, UploadFile
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List, Dict, Union
import os
from dotenv import load_dotenv

load_dotenv()

class SpeechRecognition(BaseModel):
    passkey : str = os.getenv("passkey")


class Word(BaseModel):
    word: str
    start: float
    end: float

class SpeechRecognitionResponse(BaseModel):
    text: str
    word_count: int
    words: List[Word]

class SuccessfulSpeechRecognition(BaseModel):
    response: SpeechRecognitionResponse

    class Config:
        json_schema_extra = {
            "example": {
                "response": {
                    "text": "Best doing one two three",
                    "word_count": 5,
                    "words": [
                        {
                            "word": "Best",
                            "start": 0.3400000035762787,
                            "end": 0.7400000095367432
                        },
                        {
                            "word": "doing",
                            "start": 0.7400000095367432,
                            "end": 1.059999942779541
                        },
                        {
                            "word": "one",
                            "start": 1.059999942779541,
                            "end": 1.600000023841858
                        },
                        {
                            "word": "two",
                            "start": 1.600000023841858,
                            "end": 1.899999976158142
                        },
                        {
                            "word": "three",
                            "start": 1.899999976158142,
                            "end": 2.3399999141693115
                        }
                    ]
                }
            }
        }