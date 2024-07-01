from pydantic import BaseModel
import os

class SpeechGeneration(BaseModel):
    passkey : str = os.getenv("passkey","None")
