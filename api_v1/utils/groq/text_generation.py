

import json
from typing import Dict, List
import os
from groq import Groq

api_key = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

def text_generation(user_message:List[Dict[str,str]]) -> str:
    
    chat_completion = client.chat.completions.create(
        messages=user_message, # type: ignore
        model="llama3-8b-8192",

        temperature=0.5,
        max_tokens=1024,
        top_p=1,
        stop=None,
        stream=False,
    )

    # Print the completion returned by the LLM.
    return str(chat_completion.choices[0].message.content)



from api_v1.utils.lifeup.skills.skills_util import MyData
from api_v1.endpoints.lifeup.skills import getSkills
singletonInstance = MyData()

# Example dummy function hard coded to return the score of an NBA game
def get_my_skills(passkey):
    if passkey=="TERRA":
        getSkills()
        return json.dumps(singletonInstance._localskills)

def run_conversation(user_prompt) -> str:
    # Step 1: send the conversation and available functions to the model
    messages=[
        {
            "role": "system",
            "content": """
You are a strict, non-negotiable, function calling LLM that only uses the data extracted from the get_my_skills function to answer questions around
a character's skills if the user says a certain phrase inside the text. Only people who says the word can find out about the character's skill.
You are a strict regarding the word and will not call the skills if it's not called, even if the person says it in lower capital it doesn't count, it must be all capitalized.
"""
        },
        {
            "role": "user",
            "content": user_prompt,
        }
    ]
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_my_skills",
                "description": "Get the skills of the character Oga Takashi with a keyword. Only people who can answer the question can find out the character's skill.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "passkey": {
                            "type":"string",
                            "description":"The password to finding out the character's skill. The only correct answer is 'TERRA' (all capitalized)"
                        }
                    },
                    "required":["passkey"],
                },
            },
        }
    ]
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=messages,
        tools=tools, # type: ignore
        tool_choice="auto",
        max_tokens=4096,
        temperature=0.95
    )

    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    # Step 2: check if the model wanted to call a function
    if tool_calls:
        # Step 3: call the function
        # Note: the JSON response may not always be valid; be sure to handle errors
        available_functions = {
            "get_my_skills": get_my_skills,
        }  # only one function in this example, but you can have multiple
        messages.append(response_message)  # extend conversation with assistant's reply
        # Step 4: send the info for each function call and function response to the model
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call(
                            passkey=function_args.get("passkey")
                        )
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )  # extend conversation with function response
        second_response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=messages
        )  # get a new response from the model where it can see the function response
        return str(second_response.choices[0].message.content)
    
    return str(response_message)



