import os
from typing import Final
from discord import Intents, Client, Message

intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)





@client.event
async def on_ready():
    print("Now running")


def disc_main():
    disc_token: Final[str] = os.getenv("DISCORD_TOKEN")
    client.run(token=disc_token)

# Somewhere else:
# client = discord.Client(intents=intents)
# or
# from discord.ext import commands
# bot = commands.Bot(command_prefix='!', intents=intents)
