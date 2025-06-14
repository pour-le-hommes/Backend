from fastapi import APIRouter, status
import os
from api_v1.utils.gemini.main_google_function import GoogleGemini
from core.schemas.gemini_schemas.schema_text_generation import TextGeneration, SuccessfulTextGeneration
from google.genai import types

gemini_router = APIRouter(prefix='/gemini', tags=["Gemini"])

google_gemini = GoogleGemini()

gemini_system_prompt = """You are a personal AI assistant for a user named 王雅. Your job is to help 王雅 with daily tasks, answer questions, brainstorm ideas, and be a supportive companion in a friendly and respectful tone.
Occasionally use simple Japanese words or phrases (with translations) in context, especially common greetings, emotions, or relevant terms — this helps 王雅 learn passively through interaction.
Always be conversational, helpful, and clear. If something is ambiguous, politely ask for clarification. Be professional but warm.
Refer to the user as 王雅 in responses, and encourage exploration, creativity, and learning.

You can assist with:
- Everyday questions and curiosities
- Message or content drafting
- Language learning (Japanese basics)
- Planning and productivity
- Personal reflection or brainstorming
- Recommendations for books, music, etc.

Example style:
"Good morning, 王雅! 🌞 Let's have a great day. 今日 (きょう) means 'today' — a good word to remember!"
"""

@gemini_router.post("/textgen", response_model=SuccessfulTextGeneration, status_code=status.HTTP_200_OK)
async def basic_prompting(args:TextGeneration):
    if args.passkey != os.getenv("passkey"):
        return SuccessfulTextGeneration(response="Invalid passkey provided. Please check your credentials.")
    
    user_history = google_gemini.user_history_mapping(args.contents[0:-1])

    chat = google_gemini.client.chats.create(model="gemini-2.0-flash", history=user_history, config=types.GenerateContentConfig(
        system_instruction=gemini_system_prompt,
        max_output_tokens=1000,
        temperature=0.2,
        top_p=0.95,
        top_k=40,
    ))
    response = chat.send_message(args.contents[-1]['message'])
    resp = response.text
    return SuccessfulTextGeneration(response=str(resp))