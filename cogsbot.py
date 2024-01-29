import discord
from discord.ext import commands
import os
import asyncio

#Import Tokens
from apikeys import *

#What the bot is interested in receiveing
intents = discord.Intents.all()
client = commands.AutoShardedBot(command_prefix = '!', intents=intents) #Initialize Bot

#Start Up
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game('Sword Art Online'))
    print("Link Start!")
    print("-----------")

#cogs
async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await client.load_extension(f'cogs.{filename[:-3]}')

async def main():
    await load()
    await client.start(TOKEN)
  
#Run
asyncio.run(main())