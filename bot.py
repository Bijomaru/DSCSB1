import discord

from utilities import utilities
from discord.ext import commands

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print(self.guilds)


    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return
        
        if message.content.startswith('!hello'):
            await message.reply('Hello {user}'.format(user=message.author.nick), mention_author=True)

client = MyClient()
client.run(utilities.token)