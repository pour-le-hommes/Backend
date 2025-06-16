from google.genai import types
from google import genai
import os
from dotenv import load_dotenv
from typing import List, Dict
from api_v1.utils.gemini.gemini_configs import memorize_information_function, recall_information_function, gemini_system_prompt
from api_v1.utils.gemini.gemini_functions import memorize_information, recall_information
from core.models.gemini_functions_models import MemorizeInformation, RecallInformation

load_dotenv()

class GoogleGemini():
    __instance__ = None
    def __new__(cls, *args, **kwargs):
        if not cls.__instance__:
            cls.__instance__ = super(GoogleGemini, cls).__new__(cls)
        return cls.__instance__
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized = True
            api_key = os.getenv("GOOGLE_GENERATIVE_AI_API_KEY")
            self.client = genai.Client(api_key=api_key)
            self.tools = types.Tool(
                function_declarations=[
                    types.FunctionDeclaration(**memorize_information_function),
                    types.FunctionDeclaration(**recall_information_function)
                ]
            )
            self.conversation_keywords : List[str] = []
            self.real_data: List[Dict[str, str]] = []
            
    def user_history_mapping(self, user_history: List[Dict[str, str]]) -> List:
        user_history_mapped = []
        
        for message in user_history:
            if message['role'] == 'user':
                user_history_mapped.append(
                    types.UserContent(parts=[types.Part.from_text(text=message['message'])])
                )
            elif message['role'] == 'model':
                user_history_mapped.append(
                    types.ModelContent(parts=[types.Part.from_text(text=message['message'])])
                )
        return user_history_mapped
    
    def generate_vector_embedding(self, text: str) -> List[types.ContentEmbedding]:
        """
        Generate vector embedding for the given text using Google Gemini API.
        
        Args:
            text (str): Text to generate embedding for.

        Returns:
            List[types.ContentEmbedding]: Vector representation of the text.
        """
        response = self.client.models.embed_content(
            model="gemini-embedding-exp-03-07",
            contents=text,
        )
        return response.embeddings if response.embeddings else []
            
    def text_generation(self, messages: List[Dict[str, str]]) -> List[Dict[str, str]]:
        user_history = self.user_history_mapping(messages[0:-1])

        chat = self.client.chats.create(
            model="gemini-2.0-flash",
            history=user_history,
            config={
                'system_instruction':gemini_system_prompt,
                'tools': [self.tools],
                'temperature':0.8
            }
        )
        response = chat.send_message(messages[-1]['message'])
        
        if not response.function_calls or len(response.function_calls)!=1:
            conv_details = [str(message.parts[0].text) for message in chat.get_history()] # type: ignore
            self.conversation_keywords = conv_details
            real_roles = []
            real_messages = []
            for message in chat.get_history():
                print('\n\n===============================')
                real_roles.append(message.role)
                real_message = message.parts[0].text # type: ignore
                if real_message == None:
                    if message.role == 'model':
                        function_call_message = f"I'm using the function tool: {message.parts[0].function_call.name} with the data: {message.parts[0].function_call.args}" # type: ignore
                        real_messages.append(function_call_message)
                        print(message.parts[0].function_call) # type: ignore
                    else:
                        function_response_message = f"Document retrieved from function call: {message.parts[0].function_response.response['result'].data[0]}" # type: ignore
                        real_messages.append(function_response_message)
                        print(message.parts[0].function_response.response['result'].data[0]) # type: ignore
                else:
                    real_messages.append(message.parts[0].text) # type: ignore
                    
            real_data = [{'role': r, 'message': m} for r, m in zip(real_roles, real_messages)]
            self.real_data = real_data
            return self.real_data
        
        tool_call = response.function_calls[0]
        if 'memorize_information'==tool_call.name:
            validated_args = MemorizeInformation(**tool_call.args) # type: ignore
            vector_embedding = self.generate_vector_embedding(validated_args.info)
            if not vector_embedding:
                raise ValueError("Failed to generate vector embedding for the provided information.")
            validated_args.embedding = vector_embedding[0].values
            result = memorize_information(validated_args)
            
        elif 'recall_information'==tool_call.name:
            validated_args = RecallInformation(**tool_call.args) # type: ignore
            vector_embedding = self.generate_vector_embedding(validated_args.info)
            if not vector_embedding:
                raise ValueError("Failed to generate vector embedding for the provided information.")
            validated_args.embedding = vector_embedding[0].values
            result = recall_information(validated_args)
        
        function_response_part = types.Part.from_function_response(
            name=str(tool_call.name),
            response={"result": result},
        )
        user_history.append(function_response_part)
        response = chat.send_message(function_response_part)
        
        conv_details = [str(message.parts[0].text) for message in chat.get_history()] # type: ignore
        self.conversation_keywords = conv_details
        
        real_roles = []
        real_messages = []
        for message in chat.get_history():
            print('\n\n===============================')
            real_roles.append(message.role)
            real_message = message.parts[0].text # type: ignore
            if real_message == None:
                if message.role == 'model':
                    function_call_message = f"I'm using the function tool: {message.parts[0].function_call.name} with the data: {message.parts[0].function_call.args}" # type: ignore
                    real_messages.append(function_call_message)
                    print(message.parts[0].function_call) # type: ignore
                else:
                    print("\n\nchecking inside message.parts[0].function_response.response['result']: ", message.parts[0].function_response.response['result']) # type: ignore
                    function_response_message = f"Document retrieved from function call: {message.parts[0].function_response.response['result']}" # type: ignore
                    real_messages.append(function_response_message)
                    print(message.parts[0].function_response.response['result']) # type: ignore
            else:
                real_messages.append(message.parts[0].text) # type: ignore
        real_data = [{'role': r, 'message': m} for r, m in zip(real_roles, real_messages)]
        self.real_data = real_data
            
        return self.real_data
