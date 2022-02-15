import discord
import os

from dotenv import load_dotenv
from wakeonlan import send_magic_packet

load_dotenv()

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('$on'):
        send_magic_packet(os.getenv('SRVMAC', ip_address='BCAST'))
        await message.channel.send('Turning server on!')

client.run(os.getenv('TOKEN'))
