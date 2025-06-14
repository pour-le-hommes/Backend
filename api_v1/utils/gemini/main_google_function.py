from io import BytesIO
from google import genai
import os
from dotenv import load_dotenv
from typing import List, Dict, Union
from google.genai import types

load_dotenv()

class GoogleGemini():
    __instance__ = None
    def __new__(cls, *args, **kwargs):
        if not cls.__instance__:
            cls.__instance__ = super(GoogleGemini, cls).__new__(cls)
        return cls.__instance__
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized = True
            api_key = os.getenv("GOOGLE_GENERATIVE_AI_API_KEY")
            self.client = genai.Client(api_key=api_key)
            
    def user_history_mapping(self, user_history: List[Dict[str, str]]):
        user_history_mapped = []
        
        for message in user_history:
            if message['role'] == 'user':
                user_history_mapped.append(
                    types.UserContent(parts=[types.Part.from_text(text=message['message'])])
                )
            elif message['role'] == 'model':
                user_history_mapped.append(
                    types.ModelContent(parts=[types.Part.from_text(text=message['message'])])
                )
        return user_history_mapped
            
    async def text_generation(self, message: str) -> str:
        """
        Generate text using Google Gemini API.
        
        Args:
            message (str): Message to send to the model.

        Returns:
            str: Generated text response.
        """
        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[message]
        )
        return str(response.text)
