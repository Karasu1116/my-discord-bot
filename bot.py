import discord
from discord.ext import commands
from discord import Interaction
from discord import app_commands
import requests
import json

#Import Tokens
from apikeys import *

#What the bot is interested in receiveing
intents = discord.Intents.all()

client = commands.Bot(command_prefix = '!', intents=intents) #Initialize Bot

#Event
@client.event
async def on_ready(): #when ready, bot will execute function
    await client.change_presence(status=discord.Status.idle, activity=discord.Game('Sword Art Online'))
    print("Link Start!")
    print("-----------")
    try:
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} command(s)") #syncing commands to boy
    except Exception as e:
        print(e)

#Slash commands
@client.tree.command(name="test")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hey {interaction.user.mention}! By order of the Peaky Blinders!" ) #ephemeral=True means only sender can see it

@client.tree.command(name="say")
@app_commands.describe(thing_to_say = "What should I say?")
async def say(interaction: discord.Interaction, thing_to_say: str):
    print(interaction.user)
    await interaction.response.send_message(f"{interaction.user.name} said: '{thing_to_say}'")

#Commands
@client.command()
async def hello(ctx): #Test function, will respond to hello
    await ctx.send("Konnichiwa")

#Members Join and Anime Quote displays
@client.event
async def on_member_join(member):

    anime_quote_url = "https://10000-anime-quotes-with-pagination-support.p.rapidapi.com/rapidHandler/random"

    headers = {
        "X-RapidAPI-Key": "a17c9fa0edmsh1b28c4ed7182320p10f6d3jsnbba68eb1d4c2",
        "X-RapidAPI-Host": "10000-anime-quotes-with-pagination-support.p.rapidapi.com"
    }

    response = requests.get(anime_quote_url, headers=headers)
    data = json.loads(response.text)

    channel = client.get_channel(BOTTEST)
    await channel.send("Konnichiwa " + str(member) + "!")
    await channel.send(f"**Anime Name:** {data['animename']}\n**Quote:** *\"{data['quote']}\"*\n**Character:** {data['character']}")

#Member Leaves
@client.event
async def on_member_remove(member):
    channel = client.get_channel(BOTTEST)
    await channel.send("Sayonara " + str(member) + "!")

#Reading Message
@client.event
async def on_message(message):
    
    if "d2" in message.content or "destiny" in message.content:
        await message.delete()
        await message.channel.send("Doth not speaketh of that horrid game hither!")
    else:
        await client.process_commands(message)
    
#Embed
@client.command()
async def embed(ctx):
    embed = discord.Embed(title="Anime", url="https://myanimelist.net", description = "We love anime", color = 0x300061)
    #embed.set_author(name="Gregeth", url="https://myanimelist.net/profile/Karasu_1116", icon_url="https://cdn.myanimelist.net/s/common/userimages/ef23d6a2-48b3-4d5d-98ec-eab47936eaba_225w?s=62a7f34c70d25191c082419fc68c40bb")
    embed.set_author(name=ctx.author.display_name, url="https://myanimelist.net/profile/Karasu_1116", icon_url=ctx.author.avatar.url) #Displays User's name and avatar
    
    #setting thumbnail
    file = discord.File("your-name.gif", filename="your-name.gif")
    embed.set_thumbnail(url="attachment://your-name.gif")

    #setting field
    embed.add_field(name="Favorite Anime", value ="Demon Slayer", inline=True)
    embed.add_field(name="Favorite Charactor", value ="Ayanokouji", inline=True)
    embed.add_field(name="Favorite Antagonist", value ="Sukuna", inline=False)
    embed.add_field(name="Favorite Music Artist", value ="RADWIMPS", inline=False)

    embed.set_footer(text="Created by Karasu1116")

    await ctx.send(file = file, embed=embed)

#Run
client.run(TOKEN)
