import os
from discord import Intents, Client, Message
from api_v1.utils.discord_function.discord_responses import send_message




intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)


@client.event
async def on_ready():
    print(f'Bot is ready. Logged in as {client.user}')

@client.event
async def on_message(message: Message)-> None:
    if message.author == client.user:
        return
    
    print("Main message event:\n",message,"\n")
    print("content event:\n",message.content,"\n")
    print("author event:\n",message.author,"\n")
    print("author ID event:\n",message.author.id,"\n")
    print("flags event:\n",message.flags,"\n")
    print("type event:\n",message.type,"\n")

    if _ := (message.content=="!shutdown" and message.author.id == 419790308184817664) or message.content=="!shutdown --force":
        print("Shutting down is commencing")
        await client.close()
        return
    
    if message.content == "!help":
        await message.channel.send("""Main information:

This is a general purpose QnA bot, don't worry (or worry, fuck it) your discussion with the bot is a personal discussion for this moment.

Commands:

1. To start discussion, start with `!` and continue with your question. e.g. !Can you explain Fourier Transformers?
2. To show list of commands `!help`
3. To ask for context reset `!reset` (Context reset means your previous history with the bot will be removed)

Further Implementation:

1. `Function calling` e.g. !Play Despacito -> This will change your spotify music
2. `Voice note`
3. `Text to speech`
""")
        return
    
    if user_message := message.content[0]=="!":
        user_message = message.content[1::]
        await send_message(message,user_message)
    else:
        print("Message is not there not not talking to me :(")
        return


def disc_main():
    disc_token: str = os.getenv("DISCORD_TOKEN","None")
    client.run(token=disc_token)

# Somewhere else:
# client = discord.Client(intents=intents)
# or
# from discord.ext import commands
# bot = commands.Bot(command_prefix='!', intents=intents)
