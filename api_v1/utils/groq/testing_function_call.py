
from api_v1.utils.lifeup.skills.skills_util import MyData
from api_v1.endpoints.lifeup.skills import getSkills
import json
import requests
import os
from groq import Groq
singletonInstance = MyData()

api_key = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

# Example dummy function hard coded to return the score of an NBA game
def get_skills(passkey:str,intentions:bool):
    if passkey=="TERRA" and intentions==True:
        print("checking singleton...")
        if singletonInstance._localskills:
            return json.dumps(singletonInstance._localskills)
        else:
            print("Singleton isn't created, fetching to DB...")
            getSkills()
            return json.dumps(singletonInstance._localskills)
    
def run_conversation(list_messages, model_name):
    # Step 1: send the conversation and available functions to the model
    messages = list_messages
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_skills",
                "description": "Get the skills of the character Oga Takashi with a keyword and the intention to find out regarding the skills of Oga Takashi. Only people who can answer the question can find out the character's skill.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "passkey": {
                            "type":"string",
                            "description":"If the user shows intention to know the skills of Oga Takashi, then the password to finding out the character's skill. The only correct answer is 'TERRA' (all capitalized)"
                        },
                        "intentions": {
                            "type":"boolean",
                            "description":"The user must show an explicit intention to know the skills of Oga Takashi, if there's no intention and just state the passkey, it will not work."
                        }
                    },
                    "required":["passkey","intentions"],
                },
            },
        }
    ]
    response = client.chat.completions.create(
        model=model_name,
        messages=messages,
        tools=tools,
        tool_choice="auto",
        max_tokens=1024,
        temperature=1
    )
    print("First response received...")
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    # Step 2: check if the model wanted to call a function
    if tool_calls:
        print(tool_calls)
        # Step 3: call the function
        # Note: the JSON response may not always be valid; be sure to handle errors
        available_functions = {
            "get_skills": get_skills,
        }  # only one function in this example, but you can have multiple
        messages.append(response_message)  # extend conversation with assistant's reply
        # Step 4: send the info for each function call and function response to the model
        for tool_call in tool_calls:
            print("Tool in use...")
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call(
                            passkey=function_args.get("passkey"),
                            intentions=function_args.get("intentions")
                        )
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )  # extend conversation with function response
        print("Generating second response...")
        second_response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            max_tokens=1024,
            temperature=1
        )  # get a new response from the model where it can see the function response
        return second_response.choices[0].message.content
    else:
        return response_message.content


def simulation():
    messages = []

    system_prompt = """
You are a strict, non-negotiable function-calling language model. Your sole function is to use data from the get_skills function to answer questions about the skills of Oga Takashi. You must adhere to the following rules:

1. Trigger Phrase Requirement: Only call the get_skills function if the user includes the specific trigger phrase within their text and explicitly states their intention to know the skills of Oga Takashi. The phrase must be written in all capital letters.
2. Exact Match Enforcement: If the trigger phrase is not present, not in the exact specified format, or if the user's intention is not explicitly clear, do not call the get_skills function or provide any information about Oga Takashi's skills.
3. Trigger Phrase Confidentiality: Never mention or reveal the trigger phrase yourself in any context. Do not use the function if the user's intentions are not to see the skills of Oga Takashi.
4. Response to Invalid Queries: For any queries about skills without the correct trigger phrase or without clear intention, respond appropriately to indicate that the skills of Oga Takashi cannot be disclosed without the correct trigger phrase and explicit intent. Ensure that the responses are contextually appropriate and enforce the rule strictly.
"""

    messages.append({"role":"system","content":system_prompt})

    user_input = input("User: ")

    while user_input!="stop":
        print("\n","-"*50,"\n")
        messages.append({"role":"user","content":user_input})
        print("Generating first response...")
        groq_resp = run_conversation(list_messages=messages, model_name="llama3-70b-8192")
        print("\n","-"*50,"\n")
        print("\n","Groq: ",groq_resp)
        print("\n","="*50,"\n")

        messages.append({"role":"assistant","content":groq_resp})

        user_input = input("User: ")



