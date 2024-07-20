# from fastapi import APIRouter, File, HTTPException, UploadFile, status
# import os
# from api_v1.utils.gemini.main_google_function import text_generation, audio_generation
# from core.schemas.gemini_schemas.schema_text_generation import TextGeneration, SuccessfulTextGeneration
# from core.schemas.gemini_schemas.schema_speech_generation import SpeechGeneration
# from core.schemas.gemini_schemas.schema_text_with_image_generation import SuccessfulTextImageGeneration, TextImageGeneration

# gemini_router = APIRouter(prefix='/gemini', tags=["Gemini"])


# @gemini_router.post("/textgen", response_model=SuccessfulTextGeneration, status_code=status.HTTP_200_OK)
# async def basic_prompting(args:TextGeneration):
#     if args.passkey== os.getenv("passkey"):
#         resp = await text_generation(args.messages)
#         return SuccessfulTextGeneration(response=resp)
    
# @gemini_router.post("/withimage", response_model=SuccessfulTextImageGeneration, status_code=status.HTTP_200_OK)
# async def with_audio_prompting(
#     image_file: UploadFile = File(..., description="Image sent by the user."),
#     args = TextImageGeneration
#     ):
#     if image_file.content_type not in ["image/jpeg", "image/png", "image/jpg", "image/*"]:
#         print("image file",image_file)
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported file type")
#     if args.passkey== os.getenv("passkey"):
        
#         image_data = await image_file.read()
#         try:
#             model_response = await text_generation_with_image(image_data=image_data,message=args.messages)
#             return SuccessfulTextImageGeneration(response=model_response)
#         except Exception as e:
#             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
#     else:
#         return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


# @gemini_router.post("/withaudio", status_code=status.HTTP_200_OK)
# async def with_audio_prompting(
#     audio_file: UploadFile = File(..., description="Compressed audio file in MP3 format."),
#     additional_prompt:str="I don't understand what this is saying, can you help me?",
#     passkey:str=os.getenv("passkey","None")
#     ):
#     if passkey== os.getenv("passkey"):

#         try:
#             model_response = await audio_generation(audio_seg=audio_file,prompt=additional_prompt)
#             return model_response
#         except Exception as e:
#             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
#     else:
#         return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)