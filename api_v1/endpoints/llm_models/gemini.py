from dataclasses import dataclass
from fastapi import APIRouter, status
import os
from api_v1.utils.gemini.main_google_function import GoogleGemini
from core.schemas.gemini_schemas.schema_text_generation import SuccessfulFullTextGeneration, TextGeneration, SuccessfulTextGeneration
from google.genai import types

gemini_router = APIRouter(prefix='/gemini', tags=["Gemini"])

google_gemini = GoogleGemini()

"""
Hey, do you remember what I preferred to be called as?

Nicee! can you remember that I'm planning to make you the best assistant ever! You'll be able to do so much with the tools I'll give you :D
"""


@gemini_router.post("/textgen", response_model=SuccessfulFullTextGeneration, status_code=status.HTTP_200_OK)
async def basic_prompting(args:TextGeneration):
    if args.passkey != os.getenv("passkey"):
        return SuccessfulTextGeneration(response="Invalid passkey provided. Please check your credentials.")
    if args.contents[-1]['message']=='!clear':
        google_gemini.real_data = []
        return
    
    check_conversation = args.contents[-2]['message']
    if check_conversation in google_gemini.conversation_keywords[1:-1]:
        print('\n\n=========================================')
        print('USING CACHED DATA')
        print('checking user message:', check_conversation)
        print('\nchecking real_data:', google_gemini.real_data)
        print('=========================================\n\n')
        google_gemini.real_data.append(args.contents[-1])
        messages = google_gemini.real_data
    else:
        messages = args.contents
        
    response = google_gemini.text_generation(messages)
    return SuccessfulFullTextGeneration(response=response)