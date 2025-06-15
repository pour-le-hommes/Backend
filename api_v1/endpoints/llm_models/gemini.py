from dataclasses import dataclass
from fastapi import APIRouter, status
import os
from api_v1.utils.gemini.main_google_function import GoogleGemini
from core.schemas.gemini_schemas.schema_text_generation import TextGeneration, SuccessfulTextGeneration
from google.genai import types

gemini_router = APIRouter(prefix='/gemini', tags=["Gemini"])

google_gemini = GoogleGemini()


@gemini_router.post("/textgen", response_model=SuccessfulTextGeneration, status_code=status.HTTP_200_OK)
async def basic_prompting(args:TextGeneration):
    if args.passkey != os.getenv("passkey"):
        return SuccessfulTextGeneration(response="Invalid passkey provided. Please check your credentials.")
    if args.contents[-1]['message']=='!clear':
        google_gemini.current_conversation = {}
        return
    
    print('\n\n=========================================')
    print('checking user message:', args.contents)
    print('checking cache:', google_gemini.current_conversation)
    print('=========================================\n\n')
    
    check_conversation = args.contents[-2]['message']
    if check_conversation in google_gemini.current_conversation['conversation_keywords']:
        print('\n\n=========================================')
        print('USING CACHED DATA')
        print('checking user message:', check_conversation)
        print('checking conversation_keywords:', google_gemini.current_conversation['conversation_keywords'])
        print('\nchecking real_data:', google_gemini.current_conversation['real_data'])
        print('=========================================\n\n')
        google_gemini.current_conversation['real_data'].append(args.contents[-1])
        messages = google_gemini.current_conversation['real_data']
    else:
        messages = args.contents
        
    response = google_gemini.text_generation(messages)
    return SuccessfulTextGeneration(response=response)