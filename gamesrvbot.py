from keep_alive import keep_alive
import nextcord
import os
import paramiko

from dotenv import load_dotenv
from wakeonlan import send_magic_packet

keep_alive()

load_dotenv()

discord = nextcord.Client()
ssh = paramiko.SSHClient()

ssh.load_system_host_keys()
key = paramiko.RSAKey.from_private_key_file((os.getenv('KEYLOC')))

commands = [ 'sudo shutdown now' ]
@nextcord.event
async def on_ready():
    print('We have logged in as {0.user}'.format(discord))

@nextcord.event
async def on_message(message):
    if message.author == nextcord.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('$on'):
        send_magic_packet ((os.getenv('SRVMAC')), ip_address=(os.getenv('BCAST')))
        await message.channel.send('Turning on server!')

    if message.content.startswith('$off'):
        try:
          ssh.connect(hostname=(os.getenv('SRV')),username=(os.getenv('SVRUSR')),pkey=key)
          await message.channel.send('Turning off server!')
          for command in commands:
            stdin, stdout, stderr = ssh.exec_command(command)
            print(stdout.read().decode())
            err = stderr.read().decode()
            if err:
              print(err)

        except:
          await message.channel.send('Cant connect to Gameserver')
        ssh.close()

    if message.content.startswith('$functions'):
        await message.channel.send('$on for turning on server.')
        await message.channel.send('$off for turning off server.')
        await message.channel.send('$Hello for a friendly message.')

nextcord.run(os.getenv('TOKEN'))
