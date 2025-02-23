
import os
import re
from fastapi import APIRouter, File, HTTPException, UploadFile, status

from api_v1.utils.docs_retrieval.document_analysis import open_pdf
from api_v1.utils.groq.text_generation import run_conversation, text_generation
from core.schemas.groq_schemas.function_calling import FunctionCalling, SuccessFunctionCalling
from core.schemas.groq_schemas.text_generation import SuccessTextGeneration, TextGeneration


groq_router = APIRouter(prefix='/groq', tags=["Groq"])

@groq_router.post("/textgen", response_model=SuccessTextGeneration, status_code=status.HTTP_200_OK)
def basic_prompting(args: TextGeneration):
        try:
                assert args.passkey == os.getenv("passkey")
                resp = text_generation(args.user_prompt)
                return SuccessTextGeneration(response=resp)
        except HTTPException as e:
                HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Invalid passkey")


@groq_router.post("/withtools", response_model=SuccessFunctionCalling, status_code=status.HTTP_200_OK)
def prompting_with_tools(args: FunctionCalling):
        try:
                assert args.passkey == os.getenv("passkey")
                resp = run_conversation(args.user_prompt)
                return SuccessFunctionCalling(response=resp)
        except HTTPException as e:
                HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Invalid passkey")
                


@groq_router.get("/test_doc", status_code=status.HTTP_200_OK)
def test_document_retrieval():
        try:
                resp = open_pdf()
                return resp
        except HTTPException as e:
                HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=e)
