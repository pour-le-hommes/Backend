import requests
import os
from dotenv import load_dotenv
from api_v1.utils.data.dict_text_gen import get_text_gen_dict, get_speech_dict
from typing import List, Dict

load_dotenv(override=True)

text_gen_model_dict = get_text_gen_dict()
speech_model_dict = get_speech_dict()

def get_list_models():
    url = f"https://api.cloudflare.com/client/v4/accounts/{os.getenv('CLOUDFLARE_API_ID')}/ai/models/search"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('CLOUDFLARE_API_KEY')}"
    }

    response = requests.request("GET", url, headers=headers)
    to_json = eval(response.text.replace("true","True"))
    return to_json["result"]


def check_api_token():
    try:
        
        url = f"https://api.cloudflare.com/client/v4/user/tokens/verify"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.getenv('CLOUDFLARE_API_KEY')}"
        }
        
        response = requests.get(url, headers=headers).json()
        
        if response.get('success') and response['result']['status'] == "active":
            print("It's working")
            return True
        else:
            return False
    except Exception as e:
        raise e


def text_generation(messages:List[Dict],model_name:int):
    API_URL = f"https://api.cloudflare.com/client/v4/accounts/{os.getenv('CLOUDFLARE_API_ID')}/ai/run/{text_gen_model_dict[model_name]}"
    headers = {
        "Authorization": f"Bearer {os.getenv('CLOUDFLARE_API_KEY')}",
        "Content-Type": "application/json"
    }
    body = {
      "messages": messages
    }

    try:
        cloudflare_response = requests.post(API_URL, headers=headers, json=body).json()
    except ConnectionRefusedError as err:
        raise err
    
    try:
        output = cloudflare_response["result"]["response"]
        return output
    except ConnectionRefusedError as err:
        raise err
     

def text_classification(messages:str):
    API_URL = f"https://api.cloudflare.com/client/v4/accounts/{os.getenv('CLOUDFLARE_API_ID')}/ai/run/@cf/huggingface/distilbert-sst-2-int8"
    headers = {
        "Authorization": f"Bearer {os.getenv('CLOUDFLARE_API_KEY')}",
        "Content-Type": "application/json"
    }
    body = {
        "text":messages
    }
    
    try:
        cloudflare_response = requests.post(API_URL, headers=headers, json=body).json()
    except ConnectionRefusedError as err:
        raise err

    try:
        output = cloudflare_response["result"]
        return output
    except ConnectionRefusedError as err:
        raise err


async def speech_recognition(audio_bytes:bytes,model_name:int):
    API_URL = f"https://api.cloudflare.com/client/v4/accounts/{os.getenv('CLOUDFLARE_API_ID')}/ai/run/{speech_model_dict[model_name]}"
    headers = {
        "Authorization": f"Bearer {os.getenv('CLOUDFLARE_API_KEY')}",
        "Content-Type": "application/octet-stream"
    }
    body = audio_bytes

    try:
        cloudflare_response = requests.post(API_URL, headers=headers, data=body).json()
    except ConnectionRefusedError as err:
        raise err

    try:
        output = cloudflare_response["result"]
        return output
    except ConnectionRefusedError as err:
        raise err
    

def text_embedding(text:str):
    API_URL = f"https://api.cloudflare.com/client/v4/accounts/{os.getenv('CLOUDFLARE_API_ID')}/ai/run/@cf/baai/bge-base-en-v1.5"
    headers = {
        "Authorization": f"Bearer {os.getenv('CLOUDFLARE_API_KEY')}",
    }
    body = {
        "text":[text]
    }

    try:
        cloudflare_response = requests.post(API_URL, headers=headers, json=body).json()
    except ConnectionRefusedError as err:
        raise err

    try:
        output = cloudflare_response["result"]["data"][0]
        return output
    except ConnectionRefusedError as err:
        raise err