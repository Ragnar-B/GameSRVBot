import discord
import os

from dotenv import load_dotenv
from wakeonlan import send_magic_packet
from paramiko import SSHClient

load_dotenv()

discord = discord.Client()
#ssh = SSHclient()

#discord.run(os.getenv('TOKEN'))
#ssh.load_system_host_keys()

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

#    if message.content.startswith('$off'):
#        ssh.connect(os.getenv('SRV'))
#        await message.channel.send('Turning off server!')
#        ssh.close()
discord.run(os.getenv('TOKEN'))
