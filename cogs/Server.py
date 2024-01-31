import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
from discord import app_commands
from discord import Member
from discord import Interaction
from discord.utils import get
import requests
import json
import os
import boto3
from dotenv import load_dotenv

intents = discord.Intents.all()
bot = commands.AutoShardedBot(command_prefix = '!', intents=intents) #Initialize Bot
ec2 = boto3.client("ec2") #Innitialize ec2

load_dotenv()

INSTANCE_ID = os.getenv("INSTANCE_ID")

class Server(commands.Cog):

    def __init__(self, client):
        self.client = client

    #Commands
    @commands.command()
    async def test(self, ctx): #Test function, will respond to hello
        await ctx.send("works")

    #testing
    @app_commands.command(name="servertest")
    async def hello(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Hey {interaction.user.mention}! I have a minecraft server!" ) #ephemeral=True means only sender can see it

    #Start_command
    @commands.command()
    async def startServer(self, ctx):
        try:
            await ctx.send("Attempting to start server...")
            ec2.start_instances(InstanceIds=[INSTANCE_ID])
            await ctx.send("Server is online!")
        except Exception as err:
            print(err)
            await ctx.send("Server is already up!")

    '''
    #Start_slash
    @bot.tree.command(name="start")
    async def start_server(self, interaction: discord.Interaction):
        try:
            await interaction.response.send_message(f"Attempting to start server...")
            ec2.start_instances(InstanceIds=[INSTANCE_ID])
            await interaction.response.send_message("Server is online!")
        except Exception as err:
            print(err)
            await interaction.response.send_message("Server is already up!")
    '''
    #Stop
    @commands.command()
    async def stopServer(self, ctx):
        try:
            await ctx.send("Attempting to shutdown server...")
            ec2.stop_instances(InstanceIds=[INSTANCE_ID])
            await ctx.send("Server shutdown complete!")
        except Exception as err:
            print(err)
            await ctx.send("Server is already off!")

    '''
    #Stop
    @bot.tree.command(name="stop")
    async def stop_server(self, interaction: discord.Interaction):
        try:
            await interaction.response.send_message(f"Attempting to shutdown server...")
            ec2.stop_instances(InstanceIds=[INSTANCE_ID])
            await interaction.response.send_message("Server shutdown complete!")
        except Exception as err:
            print(err)
            await interaction.response.send_message("Server is already off!")
    '''
    

async def setup(client):
    await client.add_cog(Server(client))