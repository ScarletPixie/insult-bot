import discord
import asyncio

from decouple import config

#   settings
TOKEN= config('BOT_TOKEN')
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

async def insult_members():
    insult = ''

    await client.wait_until_ready()
    guild = client.get_guild(config('SERVER_ID'))

    while not client.is_closed():

        for member in guild.members:
            if member.bot:
                continue
            try:
                await member.send(insult)
            except discord.Forbidden:
                print(f"Couldn't send message to {member.name}")

@client.event
async def on_ready():
    print(f'logged in as {client.user}')
    client.loop.create_task()