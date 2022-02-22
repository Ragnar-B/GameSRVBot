import discord
import os
import paramiko

from dotenv import load_dotenv
from wakeonlan import send_magic_packet

load_dotenv()

discord = discord.Client()
ssh = paramiko.SSHClient()

ssh.load_system_host_keys()

shtdwncmd = "shutdown -h now"

@discord.event
async def on_ready():
    print('We have logged in as {0.user}'.format(discord))

@discord.event
async def on_message(message):
    if message.author == discord.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('$on'):
        send_magic_packet ((os.getenv('SRVMAC')), ip_address=(os.getenv('BCAST')))
        await message.channel.send('Turning on server!')

    if message.content.startswith('$off'):
        try:
          ssh.connect(hostname=(os.getenv('SRV')))
          await message.channel.send('Turning off server!')
        except:
          await message.channel.send('Cant connect to Gameserver')
        ssh.close()

discord.run(os.getenv('TOKEN'))
