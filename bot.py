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

# bot = commands.Bot(command_prefix='!')

def find_invite_by_code(self, invite_list, code):
    return [inv for inv in invite_list if inv.code == code][0]

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print(self.guilds)
        guild = self.guilds[0]
        if guild.name == 'Social Cooking':
            await self.guilds[0].system_channel.send('Bot connected')
        current_invites = await guild.invites()

    async def on_member_join(self, member):
        guild = member.guild
        updated_invites = await member.guild.invites()
        for invite in current_invites:
            if invite.uses < find_invite_by_code(updated_invites, invite.code).uses:
                print(f"Member {member.name} Joined")
                print(f"Invite Code: {invite.code}")
                print(f"Inviter: {invite.inviter}")
                current_invites = updated_invites
                return


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

            role = await guild.create_role(name=session_name, permissions = discord.Permissions._from_value(103812608))

            cat = await guild.create_category_channel(session_name)
            
            overwrite = discord.PermissionOverwrite()
            overwrite.view_channel = False
            await cat.set_permissions(guild.default_role, overwrite=overwrite)

            overwrite = discord.PermissionOverwrite()
            overwrite.view_channel = True
            await cat.set_permissions(message.author, overwrite=overwrite)
            await cat.set_permissions(role, overwrite=overwrite)

            txt = await cat.create_text_channel('Text')
            vc = await cat.create_voice_channel('Voice')
            invite_txt = await txt.create_invite(max_uses=10, unique=True, temporary=True, reason='')
            invite_vc = await vc.create_invite(max_uses=10, unique=True, temporary=True, reason='')
            
            await txt.send(invite_txt)
            await txt.send(invite_vc)
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

            await discord.utils.get(guild.roles, name=session_name).delete()

            await message.reply('Session {session} ended'.format(session=session_name), mention_author=True)
            await guild.system_channel.send('Session {session} ended'.format(session=session_name))
            return

        if message.content.startswith('!hello'):
            await message.reply('Hello {user}'.format(user=user), mention_author=True)
            return
 

        if message.content.startswith('!guide'):
            await message.reply(guide_txt)
            return



intents = discord.Intents.default()
intents.members = True

client = MyClient()
client.run(utilities.token)