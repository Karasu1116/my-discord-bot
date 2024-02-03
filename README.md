# Discord bot for a Minecraft server
Hosted a Minecraft server on an EC2 Instance with AWS and Docker.

## Bot Functionality
Rather than the host of the EC2 Instance having to log into their
AWS account to toggle the Minecraft Server when someone wants to play
or after they leave, anyone can toggle it with this bot!

The bot allows members of the Minecraft Server to toggle the EC2 Instance
with simple commands /start and /stop in a discord server. This allows
members to not have to constantly ask the owner of the server to turn it
on for them. This also is a cost-effective way to host a minecraft server
with the ability for any member to turn the server off rather than keep
it up when no one is on.

TODO: Give the bot the ability to monitor player activity and shutdown the
EC2 Instance when no one has been active for ~30 minutes.

## Docker
Docker setup: https://github.com/itzg/docker-minecraft-server
