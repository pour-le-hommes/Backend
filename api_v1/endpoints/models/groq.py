
from fastapi import APIRouter, File, HTTPException, UploadFile, status

from api_v1.utils.groq.text_generation import run_conversation, text_generation


groq_router = APIRouter(prefix='/groq', tags=["Groq"])

@groq_router.post("/textgen", status_code=status.HTTP_200_OK)
def basic_prompting():
        resp = text_generation()
        return resp


@groq_router.post("/withtools", status_code=status.HTTP_200_OK)
def prompting_with_tools():
    user_prompt = "What are my skills?"
    return run_conversation(user_prompt)
