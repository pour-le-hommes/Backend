import google.generativeai as genai
import os
from dotenv import load_dotenv
from pydub import AudioSegment

load_dotenv()

async def text_generation(prompt:str):
    api_key = os.getenv("GENAI_TEST_API_KEY") or  os.getenv("GOOGLE_GENERATIVE_AI_API_KEY")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name='gemini-1.5-flash')
    resp = model.generate_content(prompt)
    genai.upload_file()
    print(resp.text)
    return resp.text


async def audio_generation(prompt:str, audio_seg:AudioSegment):
    api_key = os.getenv("GENAI_TEST_API_KEY") or  os.getenv("GOOGLE_GENERATIVE_AI_API_KEY")
    genai.configure(api_key=api_key)

    

    content = [
        "Please transcribe this recording:",
        {
            "mime_type": "audio/mp3",
            "data": audio_seg[:10000].export().read()
        }
    ]

    model = genai.GenerativeModel(model_name='gemini-1.5-flash')
    resp = model.generate_content(prompt)
    genai.upload_file()
    print(resp.text)
    return resp.text