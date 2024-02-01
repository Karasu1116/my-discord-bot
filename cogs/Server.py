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
MC_CHANNEL_ID = os.getenv("MC_CHANNEL_ID")

#SSM makes ec2 run commands in aws linux terminal
docker_start_command = ['docker start 68ab44d8e083']

class Server(commands.Cog):

    def __init__(self, client):
        self.client = client

    #Start
    @bot.tree.command(name="start")
    async def start_server(self, interaction: discord.Interaction):
            try:
                if interaction.channel_id == int(MC_CHANNEL_ID):
                    ec2.start_instances(InstanceIds=[INSTANCE_ID])
                    await interaction.response.send_message("Server is online!")
                else:
                    await interaction.response.send_message("You do not have permission to use this command!")
            except Exception as err:
                print(err)
                await interaction.response.send_message("An error occured!")

    #Stop_slash
    @bot.tree.command(name="stop")
    async def stop_server(self, interaction: discord.Interaction):
        try:
            if interaction.channel_id == int(MC_CHANNEL_ID):
                ec2.stop_instances(InstanceIds=[INSTANCE_ID])
                await interaction.response.send_message("Server shutdown complete!")
            else:
                await interaction.response.send_message("You do not have permission to use this command!")
        except Exception as err:
            print(err)
            await interaction.response.send_message("An error occured!")
    

async def setup(client):
    await client.add_cog(Server(client))