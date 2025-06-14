import requests
import os
from dotenv import load_dotenv
from api_v1.utils.data.dict_text_gen import get_text_gen_dict, get_speech_dict
from typing import List, Dict

class CloudflareAPI:
    _instance = None
    text_gen_model_dict : Dict[int, str] = {}
    speech_model_dict : Dict[int, str] = {}
    api_id = ""
    api_key = ""

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CloudflareAPI, cls).__new__(cls)
            load_dotenv(override=True)
            cls._instance.text_gen_model_dict = get_text_gen_dict()
            cls._instance.speech_model_dict = get_speech_dict()
            cls._instance.api_id = os.getenv('CLOUDFLARE_API_ID')
            cls._instance.api_key = os.getenv('CLOUDFLARE_API_KEY')
        return cls._instance

    def get_list_models(self):
        url = f"https://api.cloudflare.com/client/v4/accounts/{self.api_id}/ai/models/search"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        response = requests.request("GET", url, headers=headers)
        to_json = eval(response.text.replace("true", "True"))
        return to_json["result"]

    def check_api_token(self):
        try:
            url = "https://api.cloudflare.com/client/v4/user/tokens/verify"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            response = requests.get(url, headers=headers).json()
            if response.get('success') and response['result']['status'] == "active":
                print("It's working")
                return True
            else:
                return False
        except Exception as e:
            raise e

    def text_generation(self, messages: List[Dict], model_name: int):
        API_URL = f"https://api.cloudflare.com/client/v4/accounts/{self.api_id}/ai/run/{self.text_gen_model_dict[model_name]}"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
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

    def text_classification(self, messages: str):
        API_URL = f"https://api.cloudflare.com/client/v4/accounts/{self.api_id}/ai/run/@cf/huggingface/distilbert-sst-2-int8"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        body = {
            "text": messages
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

    async def speech_recognition(self, audio_bytes: bytes, model_name: int):
        API_URL = f"https://api.cloudflare.com/client/v4/accounts/{self.api_id}/ai/run/{self.speech_model_dict[model_name]}"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
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

    def text_embedding(self, text: str):
        API_URL = f"https://api.cloudflare.com/client/v4/accounts/{self.api_id}/ai/run/@cf/baai/bge-base-en-v1.5"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
        }
        body = {
            "text": [text]
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

# Usage:
# cloudflare_api = CloudflareAPI()
# result = cloudflare_api.get_list_models()
