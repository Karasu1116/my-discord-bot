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

## Docker
Docker setup for Minecraft: https://github.com/itzg/docker-minecraft-server

### Commands used for docker to start up a Minecraft Server on AWS
sudo yum install docker
sudo gpasswd -a ec2-user docker

sudo systemctl enable docker.service
sudo systemctl enable containerd.service

sudo systemctl start docker

docker pull itzg/minecraft-server:latest
docker stop mc
docker rm mc
docker run -d --restart unless-stopped \
    -v /home/ec2-user/minecraft-server:/data \
    -p 25565:25565 \
    -e TYPE=PAPER -e EULA=TRUE -e MEMORY=3G \
    --name mc itzg/minecraft-server:latest

### Access Minecraft Server command line to use commands such as "Op player-name"
docker exec -i container-name rcon-cli

## EC2 Instance Alarm (For when users forget to shutdown the server)
Established an EC2 Instance alarm to track CPU Utilization. In the event 
that CPU Utilization dips below 7% for two consecutive 5-minute intervals, 
the server will be automatically shut down. This proactive measure is 
implemented to safeguard against instances where users inadvertently 
leave the server running upon logging off. This scenario typically occurs 
when players exit the game, resulting in a decrease in CPU Utilization below 
the specified threshold.
