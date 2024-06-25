import asyncio
import os
from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status
from fastapi.responses import RedirectResponse,JSONResponse
from api_v1.api import init_db
from api_v1.utils.cloudflare.main_function_cloudflare import get_list_models, text_generation, check_api_token, text_classification, speech_recognition
from api_v1.utils.cloudflare.add_function_cloudflare import audio_to_string
from core.schemas.cf_schemas.schema_text_generation import TextGeneration, SuccessfulGeneration
from core.schemas.cf_schemas.schema_text_classification import ClassificationResponse, TextClassification, SuccessfulClassification
from core.schemas.cf_schemas.schema_speech_recognition import SpeechRecognition, SuccessfulSpeechRecognition
from typing import List

cf_router = APIRouter(prefix='/cf', tags=["Cloudflare"])

@cf_router.get("/check_token")
def check_token():
    try:
        resp = check_api_token()
        return resp
    except ConnectionError:
        status.HTTP_400_BAD_REQUEST
    except asyncio.CancelledError:
        print("Task was cancelled, cleaning up")
    finally:
        print("Cleanup complete")

@cf_router.get("/model_list")
def model_list() -> List[object]:
    model_list = get_list_models()
    if model_list!=None:

        text_gen_models = [i for i in model_list if i["task"]["name"]=="Text Generation"]

        return text_gen_models
    else:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)
    

# ? Text Generation Model
@cf_router.post("/textgen/{model}/prompt",response_model=SuccessfulGeneration, status_code=status.HTTP_200_OK)
def text_gen_model(args:TextGeneration,model:int=0):
    if args.passkey== os.getenv("passkey"):
        try:
            model_response = text_generation(messages=args.messages, model_name=model)
            return SuccessfulGeneration(response=model_response)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    else:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong passkey Bro")


# ? Text Classification Model
@cf_router.post("/text_class/prompt",response_model=SuccessfulClassification, status_code=status.HTTP_200_OK)
def text_class_model(args:TextClassification):
    if args.passkey== os.getenv("passkey"):
        try:
            model_response = text_classification(messages=args.prompt)
            return SuccessfulClassification(
                response=ClassificationResponse(
                    text=args.prompt,
                    classification=model_response
                )
            )
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    else:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong passkey Bro")
    

# ? Speech Recognition Model
@cf_router.post("/speech/{model}/prompt",response_model=SuccessfulSpeechRecognition, status_code=status.HTTP_200_OK)
async def speech_model(passkey:str=Form(SpeechRecognition.model_fields['passkey'].default), audio_file: UploadFile = File(..., description="Compressed audio file in MP3 format."), model:int=0):
    if passkey== os.getenv("passkey"):
        if audio_file.content_type not in ["audio/mpeg", "audio/ogg"]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported file type")
        
        try:
            audio_bytes = await audio_to_string(audio_file)
            model_response = await speech_recognition(audio_bytes=audio_bytes,model_name=model)
            return SuccessfulSpeechRecognition(response=model_response)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    else:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong passkey Bro")