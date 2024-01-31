import discord
from discord.ext import commands
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

#What the bot is interested in receiveing
intents = discord.Intents.all()
bot = commands.AutoShardedBot(command_prefix = '!', intents=intents) #Initialize Bot

TOKEN = os.getenv("TOKEN")

#Start Up
@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game('Sword Art Online'))
    print("Link Start!")
    print("-----------")

#cogs
async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')

async def main():
    await load()
    await bot.start(TOKEN)
    await bot.tree.sync()
  
#Run
asyncio.run(main())