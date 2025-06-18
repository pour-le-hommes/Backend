import json
from typing import Dict, List, Any, Union
from dotenv import load_dotenv
from api_v1.utils.gemini.gemini_configs import memorize_information_function, recall_information_function, gemini_system_prompt
from api_v1.utils.gemini.gemini_functions import memorize_information, recall_information
import os
from litellm import Usage, completion
from litellm.types.utils import ModelResponse
from api_v1.utils.supabase_db.supabase_main import SupabaseDB

supadb = SupabaseDB()

os.getenv("GEMINI_API_KEY")
os.getenv("GROQ_API_KEY")

load_dotenv()


class AgnosticLLM():
    __instance__ = None
    def __new__(cls, *args, **kwargs):
        if not cls.__instance__:
            cls.__instance__ = super(AgnosticLLM, cls).__new__(cls)
        return cls.__instance__
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized = True
            self.gemini_model = "gemini/gemini-2.0-flash"
            self.groq_model = "groq/llama-3.1-8b-instant"
            
    def send_logs(self, response_data):
    
        # Access usage from the correct location if available
        token_size = response_data.usage
        if token_size is not None:
            token_size = token_size.total_tokens
        else:
            token_size = 0  # or handle as appropriate

        model_name = response_data.model
        response = response_data.choices[0].message.content
        data = {
            "response" : response,
            "model_name" : model_name,
            "token_size" : token_size,
        }
        
        supadb.insert("LLM_History", data)
            
    def text_generation(self, messages: List[Dict[str, Any]]) -> List[Dict[str, str]]: # type: ignore
        tools = [recall_information_function, memorize_information_function]
        system_prompt = {
            'role':'system',
            'content':gemini_system_prompt
        }
        
        if not any([i for i in messages if i['role']=='system']):
            messages.insert(0, system_prompt)

        response = completion(
        model=self.groq_model,
        messages=messages,
        tools=tools,
        tool_choice="auto",
        ).choices[0].message # type: ignore
        
        if not response.tool_calls:
            result_check = response.json()
            messages.append(result_check) # type: ignore
            return messages
        
        available_functions = {
            "memorize_information": memorize_information,
            "recall_information": recall_information,
        }
        result_check = response.json()
        messages.append(result_check) # type: ignore
        
        for tool_call in response.tool_calls:
            function_name = str(tool_call.function.name)
            function_to_call = available_functions[str(function_name)]
            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call(**function_args) # type: ignore
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": str(function_response),
                }
            )  # extend conversation with function response
        print('\n\nUSING FUNCTION CALLING')
        second_response = completion(
        model=self.groq_model,
        messages=messages,
        ).choices[0].message # type: ignore
        
        messages.append(second_response) # type: ignore
        print(messages)
        return messages
