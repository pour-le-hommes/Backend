from dataclasses import dataclass, field
from discord import Message
from typing import Dict, Any
import json
import requests
import os
from groq import Groq

api_key = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)


user_contexts = {}

@dataclass
class UserContext:
    user_id: int
    user_name: str
    user_messages: list = field(default_factory=list)

def create_context(message: Message)-> UserContext:
    username =  str(message.author)
    user_message = str(message.content)
    userid = int(message.author.id)

    print("Creating context for User: {} User_message: {} Authoer Id: {}".format(username,user_message, userid))

    return UserContext(user_id=userid, user_name=username)

async def get_response(message_context: list) -> str:
    chat_completion = client.chat.completions.create(
        messages=message_context,
        model="llama3-8b-8192",

        # Controls randomness: lowering results in less random completions.
        # As the temperature approaches zero, the model will become deterministic
        # and repetitive.
        temperature=0.85,

        # The maximum number of tokens to generate. Requests can use up to
        # 32,768 tokens shared between prompt and completion.
        max_tokens=150,

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
    return str(chat_completion.choices[0].message.content)

async def send_message(message: Message, user_message: str) -> None:
    """
    User_message already removed the '!'

    For example, the command !reset will just be reset.
    """
    if message.author.id not in user_contexts or user_message=="reset":
        user_contexts[message.author.id] = create_context(message=message)
        user_contexts[message.author.id].user_messages = [{"role": "system","content": "you are a helpful assistant that answers in two or three paragrahs, if the question or request is too complex answer in the same two or three paragraphs and disclose regarding the limitations. The user can ask for more detail if it's specified. The general context mainly revolves around general information and Dota 2"}]
        if user_message == "reset":
            await message.channel.send("Your context has been reset.")
            return

    user_context = user_contexts[message.author.id]
    user_context.user_messages.append({"role": "user","content": user_message})

    try:
        response: str = await get_response(user_context.user_messages)
        user_context.user_messages.append({"role": "assistant","content": response})
        await message.channel.send(response)    
    except Exception as e:
        raise e