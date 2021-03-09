import discord

from utilities import utilities
from discord.ext import commands

guide_txt = '''
This is the guide with the commands.
    !hello - responds to you with your name.
    !guide - shows these commands
    !start_session - creates new cooking session using you as host
    !end_session - ends your session
'''

bot = commands.Bot(command_prefix='!')

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print(self.guilds)
        guild = self.guilds[0]
        # if guild.name == 'Social Cooking':
        #     await self.guilds[0].system_channel.send('Bot connected')

    async def on_member_join(self, member):
        guild = member.guild
        if guild.system_channel is not None:
            to_send = 'Welcome {member.mention} to {guild.name}!'.format(member, guild)
            await guild.system_channel.send(to_send)


    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        guild = message.author.guild

        if message.author.nick:
            user = message.author.nick
        else:
            user = message.author.name

        if message.content.startswith('!test'):
            await guild.system_channel.send('test something')
            return

        if message.content.startswith('!start_session'):

            session_name = '{user}\'s cooking session'.format(user=user)

            cat = discord.utils.get(guild.categories, name=session_name)

            if cat:
                await message.reply('Session {session} already exists'.format(session=session_name), mention_author=True)
                return

            await guild.create_category_channel(session_name)

            cat = discord.utils.get(guild.categories, name=session_name)

            await cat.create_text_channel('Text')
            await cat.create_voice_channel('Voice')
            await message.reply('Session {session} has been created.'.format(session=session_name), mention_author=True)
            await guild.system_channel.send('Session {session} has been created'.format(session=session_name))

            return
        
        if message.content.startswith('!end_session'):

            session_name = '{user}\'s cooking session'.format(user=user)

            cat = discord.utils.get(guild.categories, name=session_name)

            if not cat:
                await message.reply('Session {session} already ended'.format(session=session_name), mention_author=True)
                return

            for channel in cat.channels:
                await channel.delete()
            await self.get_channel(cat.id).delete()
            await message.reply('Session {session} ended'.format(session=session_name), mention_author=True)
            await guild.system_channel.send('Session {session} ended'.format(session=session_name))
            return


            # await guild.create_category_channel(session_name)
            # await message.reply('Session {session} has been created.'.format(session=session_name), mention_author=True)
            
            return


        if message.content.startswith('!hello'):
            await message.reply('Hello {user}'.format(user=user), mention_author=True)
            return
 

        if message.content.startswith('!guide'):
            await message.reply(guide_txt)
            return

client = MyClient()
client.run(utilities.token)