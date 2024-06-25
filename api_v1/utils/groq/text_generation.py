

import json
import requests
import os
from groq import Groq

api_key = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

def text_generation():
    chat_completion = client.chat.completions.create(
        #
        # Required parameters
        #
        messages=[
            # Set an optional system message. This sets the behavior of the
            # assistant and can be used to provide specific instructions for
            # how it should behave throughout the conversation.
            {
                "role": "system",
                "content": "you are a helpful assistant."
            },
            # Set a user message for the assistant to respond to.
            {
                "role": "user",
                "content": "Explain the importance of fast language models",
            }
        ],

        # The language model which will generate the completion.
        model="llama3-8b-8192",

        #
        # Optional parameters
        #

        # Controls randomness: lowering results in less random completions.
        # As the temperature approaches zero, the model will become deterministic
        # and repetitive.
        temperature=0.5,

        # The maximum number of tokens to generate. Requests can use up to
        # 32,768 tokens shared between prompt and completion.
        max_tokens=1024,

        # Controls diversity via nucleus sampling: 0.5 means half of all
        # likelihood-weighted options are considered.
        top_p=1,

        # A stop sequence is a predefined or user-specified text string that
        # signals an AI to stop generating content, ensuring its responses
        # remain focused and concise. Examples include punctuation marks and
        # markers like "[end]".
        stop=None,

        # If set, partial message deltas will be sent.
        stream=False,
    )

    # Print the completion returned by the LLM.
    print(chat_completion)
    return chat_completion.choices[0].message.content



from api_v1.utils.lifeup.skills.skills_util import MyData
from api_v1.endpoints.lifeup.skills import getSkills
singletonInstance = MyData()

# Example dummy function hard coded to return the score of an NBA game
def get_my_skills(passkey):
    if passkey=="TERRA":
        getSkills()
        return json.dumps(singletonInstance._localskills)

def run_conversation(user_prompt):
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
        tools=tools,
        tool_choice="auto",
        max_tokens=4096,
        temperature=0.95
    )

    response_message = response.choices[0].message
    print(response.choices)
    print("\n\n\n\n")
    print(response.choices[0])
    print("\n\n\n\n")
    print(response_message.tool_calls)
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
        return second_response.choices[0].message.content



