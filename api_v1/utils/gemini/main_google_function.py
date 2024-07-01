from io import BytesIO
import google.generativeai as genai
import os
from dotenv import load_dotenv
from pydub import AudioSegment
from PIL import Image
from typing import List, Dict, Union

load_dotenv()

async def text_generation(message:List[Dict[str,Union[str,str]]]) -> str:
    api_key = os.getenv("GENAI_TEST_API_KEY") or  os.getenv("GOOGLE_GENERATIVE_AI_API_KEY")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name='gemini-1.5-flash')
    resp = model.generate_content(message)
    return str(resp.text)


async def text_generation_with_image(message:List[Dict[str,Union[str,any]]],image_data:bytes) -> str: # type: ignore
    api_key = os.getenv("GENAI_TEST_API_KEY") or  os.getenv("GOOGLE_GENERATIVE_AI_API_KEY")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name='gemini-1.5-flash')
    image = Image.open(BytesIO(image_data))
    
    
    message.append({
        "role":"user",
        "parts":[image]
    })
    resp = model.generate_content(message)
    print("response model",resp)
    return str(resp.text)


async def audio_generation(prompt:str, audio_seg:bytes):
    api_key = os.getenv("GENAI_TEST_API_KEY") or  os.getenv("GOOGLE_GENERATIVE_AI_API_KEY")
    genai.configure(api_key=api_key)

    content = [
        "Please transcribe this recording:",
        {
            "mime_type": "audio/mp3",
            "data": audio_seg[:10000].export().read() # type: ignore
        }
    ]

    model = genai.GenerativeModel(model_name='gemini-1.5-flash')
    resp = model.generate_content(prompt)
    # genai.upload_file()
    print(resp.text)
    return resp.text