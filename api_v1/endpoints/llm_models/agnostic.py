from fastapi import APIRouter, HTTPException, status
from api_v1.utils.litellm_utils.agnostic_main_function import AgnosticLLM
from core.schemas.gemini_schemas.schema_text_generation import SuccessfulFullTextGeneration, TextGeneration
import os
agnostic_router = APIRouter(prefix='/llm', tags=["Agnostic LLMs"])

agnostic_llm = AgnosticLLM()

@agnostic_router.post("/textgen", status_code=status.HTTP_200_OK)
async def basic_prompting(args:TextGeneration):
    if args.passkey != os.getenv('passkey'):
        return HTTPException(status_code=400, detail='Wrong Passkey. 誰かお前。')
      
    response = agnostic_llm.text_generation(messages=args.contents)
    print('\n\nChecking response from model:', response)
    return {'response':response}