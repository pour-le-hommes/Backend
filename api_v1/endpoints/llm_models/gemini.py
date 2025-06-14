from fastapi import APIRouter, status
import os
from api_v1.utils.gemini.main_google_function import GoogleGemini
from core.schemas.gemini_schemas.schema_text_generation import TextGeneration, SuccessfulTextGeneration

gemini_router = APIRouter(prefix='/gemini', tags=["Gemini"])

google_gemini = GoogleGemini()

@gemini_router.post("/textgen", response_model=SuccessfulTextGeneration, status_code=status.HTTP_200_OK)
async def basic_prompting(args:TextGeneration):
    if args.passkey== os.getenv("passkey"):
        resp = await google_gemini.text_generation(args.message)
        return SuccessfulTextGeneration(response=resp)