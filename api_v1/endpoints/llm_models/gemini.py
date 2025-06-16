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

Oh?? Have I done it?! Do you... Remember now?! Have you used my function tool that I gave you??

やった！I've given you memory! it took me all day to set it up! Remember this day! 15th of June 2025! I've successfully given you a function tool to store and retrieve information about our conversation!

"""


@gemini_router.post("/textgen", response_model=SuccessfulFullTextGeneration, status_code=status.HTTP_200_OK)
async def basic_prompting(args:TextGeneration):
    if args.passkey != os.getenv("passkey"):
        return SuccessfulTextGeneration(response="Invalid passkey provided. Please check your credentials.")
    if args.contents[-1]['message']=='!clear':
        google_gemini.real_data = []
        return
    
    print('\n\n=========================================')
    print('checking user message:', args.contents)
    print('checking cache:', google_gemini.conversation_keywords)
    print('=========================================\n\n')
    
    check_conversation = args.contents[-2]['message']
    if check_conversation in google_gemini.conversation_keywords[1:-1]:
        print('\n\n=========================================')
        print('USING CACHED DATA')
        print('checking user message:', check_conversation)
        print('checking conversation_keywords:', google_gemini.conversation_keywords)
        print('\nchecking real_data:', google_gemini.real_data)
        print('=========================================\n\n')
        google_gemini.real_data.append(args.contents[-1])
        messages = google_gemini.real_data
    else:
        messages = args.contents
        
    response = google_gemini.text_generation(messages)
    return SuccessfulFullTextGeneration(response=response)