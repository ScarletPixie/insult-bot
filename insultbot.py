import discord
import asyncio
import requests

from decouple import config

TOKEN=config('BOT_TOKEN')
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

async def insult_members():
    await client.wait_until_ready()
    guild = client.get_guild(config('SERVER_ID', cast=int))

    while not client.is_closed():
        insult = await get_insult()
        for member in guild.members:
            if member.bot:
                continue
            try:
                await member.send(insult)
            except discord.Forbidden:
                pass
        await asyncio.sleep(60)

@client.event
async def on_ready():
    print(f'logged in as {client.user}')
    client.loop.create_task(insult_members())

async def get_insult():
    try:
        response = requests.get('https://evilinsult.com/generate_insult.php?lang=en&type=json')
        if response.status_code != 200:
            return ''
        data = response.json()
        return data['insult']
    except requests.exceptions.RequestException as e:
        return ''

client.run(TOKEN)