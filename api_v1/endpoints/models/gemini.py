import asyncio
import io
from fastapi import APIRouter, File, HTTPException, UploadFile, status
from api_v1.api import init_db
import requests
from pydub import AudioSegment
import os
from api_v1.utils.gemini.main_google_function import text_generation, audio_generation
from core.schemas.gemini_schemas.text_generation import TextGeneration, SuccessTextGeneration
from core.schemas.gemini_schemas.speech_generation import SpeechGeneration
from typing import List
from typing import Annotated

gemini_router = APIRouter(prefix='/gemini', tags=["Gemini"])


@gemini_router.post("/textgen", response_model=SuccessTextGeneration, status_code=status.HTTP_200_OK)
async def basic_prompting(args:TextGeneration):
    if args.passkey== os.getenv("passkey"):
        resp = await text_generation(args.user_prompt)
        return SuccessTextGeneration(response=resp)
    

@gemini_router.post("/withaudio", status_code=status.HTTP_200_OK)
async def with_audio_prompting(
    audio_file: Annotated[bytes, File()],
    additional_prompt:str="I don't understand what this is saying, can you help me?",
    passkey:str=os.getenv("passkey","None")
    ):
    if passkey== os.getenv("passkey"):

        try:
            model_response = await audio_generation(audio_seg=audio_file,prompt=additional_prompt)
            return model_response
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    else:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)