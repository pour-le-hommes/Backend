import json
from typing import Dict, List, Any
from dotenv import load_dotenv
from api_v1.utils.gemini.gemini_configs import memorize_information_function, recall_information_function, gemini_system_prompt
from api_v1.utils.gemini.gemini_functions import memorize_information, recall_information
import os
from litellm import completion, embedding


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
            
    def text_generation(self, messages: List[Dict[str, Any]]) -> List[Dict[str, str]]: # type: ignore
        tools = [recall_information_function, memorize_information_function]
        system_prompt = {
            'role':'system',
            'content':gemini_system_prompt
        }
        messages.insert(0, system_prompt)

        response = completion(
        model=self.gemini_model,
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
        model=self.gemini_model,
        messages=messages,
        ).choices[0].message # type: ignore
        
        messages.append(second_response) # type: ignore
        print(messages)
        return messages
