import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
from discord import Member
from discord.utils import get
import requests
import json
from apikeys import *

intents = discord.Intents.all()
client = commands.AutoShardedBot(command_prefix = '!', intents=intents) #Initialize Bot

class Practice(commands.Cog):
    
    def __init__(self, client):
        self.client = client

    #Commands
    @commands.command()
    async def hello(self, ctx): #Test function, will respond to hello
        await ctx.send("Konnichiwa")

    #Members Join and Anime Quote displays (Event)
    @commands.Cog.listener()
    async def on_member_join(self, member):

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
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = client.get_channel(BOTTEST)
        await channel.send("Sayonara " + str(member) + "!")

    #Reading Message
    @commands.Cog.listener()
    async def on_message(self, message):
        
        if "d2" in message.content or "destiny" in message.content:
            await message.delete()
            await message.channel.send("Doth not speaketh of that horrid game hither!")
        else:
            await client.process_commands(message)
        
    #Embed
    @commands.command()
    async def embed(self, ctx):
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

    #Reactions
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user == self.client.user:
            return
        else:
            channel = reaction.message.channel
            await channel.send(user.name + " added: " + reaction.emoji)
        
    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        channel = reaction.message.channel
        await channel.send(user.name + " removed: " + reaction.emoji)

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author == self.client.user:
            return
        if "lmao" in message.content:
            emoji = '\U0001F602'
            await message.add_reaction(emoji)
    
    #Roles
    @commands.command()
    @commands.has_permissions(manage_roles = True)
    async def addRole(self, ctx, user : discord.Member, *, role : discord.Role):
        if role in user.roles:
            await ctx.send(f"{user.mention} already has the role, {role}")
        else:
            await user.add_roles(role)
            await ctx.send(f"Added {role} to {user.mention}")

            ''' testing purposes
            try:
                await user.add_roles(role)
                print("Role added successfully")
                await ctx.send(f"Added {role} to {user.mention}")
            except Exception as e:
                print(f"Error adding role: {e}")
                await ctx.send(f"An error occurred while adding {role} to {user.mention}")
            '''
    
    @addRole.error
    async def role_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have permission to use this command")

    @commands.command()
    @commands.has_permissions(manage_roles = True)
    async def removeRole(self, ctx, user : discord.Member, *, role : discord.Role):
        
        if role in user.roles:
            await user.remove_roles(role)
            await ctx.send(f"Removed {role} from {user.mention}")
        else:
            await ctx.send(f"{user.mention} does not have {role}")
    
    @removeRole.error
    async def removeRole_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have permission to use this command")

async def setup(client):
    await client.add_cog(Practice(client))