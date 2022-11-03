from keep_alive import keep_alive
import nextcord
import os
import paramiko

from wakeonlan import send_magic_packet

keep_alive()

discord = nextcord.Client()
ssh = paramiko.SSHClient()

ssh.load_system_host_keys()
key = paramiko.RSAKey.from_private_key_file("/usr/src/app/ssh.key")

ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

commands = [ 'sudo shutdown now' ]
@discord.event
async def on_ready():
    print('We have logged in as {0.user}'.format(discord))

@discord.event
async def on_message(message):
    if message.author == nextcord.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('$on'):
        send_magic_packet ((os.environ['SERVERMAC']), ip_address=(os.environ['BROADCAST']))
        await message.channel.send('Turning on server!')

    if message.content.startswith('$off'):
        try:
          ssh.connect(hostname=(os.environ['SERVER']),username=(os.environ['SERVERUSER']),pkey=key)
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

discord.run(os.environ['TOKEN'])
