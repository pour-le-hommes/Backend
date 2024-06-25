from fastapi import UploadFile
import base64

async def audio_to_string(audio_file:UploadFile):
    try:
            audio_bytes = await audio_file.read()
            return audio_bytes
    except ConnectionRefusedError as err:
        raise err