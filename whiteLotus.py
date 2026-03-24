import discord
# from discord.ext import menus  
import asyncio
import re
import requests
import io
import random
from datetime import datetime, timedelta, timezone


class WhiteLotus(object):
    

    def __init__(self):
        # self.rockchannels = [1351488087510876261]
        # self.treeandflowerchannels = [1350902682872713327, 1351488117088980992]
        # self.gatheringchannels = self.rockchannels + self.treeandflowerchannels
        # self.lootchannels = [1351438677825552435, 1351490710972534796]
        self.emojAN = ['🇦', '🇧', '🇨', '🇩', '🇪', '🇫', '🇬', '🇭', '🇮', '🇯', '🇰', '🇱', '🇲', '🇳', '🇴', '🇵', '🇶', '🇷', '🇸', '🇹', '🇺', '🇻', '🇼', '🇽', '🇾', '🇿', '0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']
        self.rollemoji = ['🔥', '🪙', '❌', '🗑️']

    def generateuniquerolls(self, n):
        if n > 100:
            toprange = n + 1
        else:
            toprange = 101
        return random.sample(range(1, toprange), n)

    async def loot(self, message):
        if not (ats := message.attachments):
            return
        
        files = []
        for x in range(len(ats)):
            at = ats[x]
            byts = requests.get(at.proxy_url).content
            file = io.BytesIO(byts)
            file.name = at.filename
            files.append(discord.File(file))

        s = ''
        if message.content:
            s += f'{message.content}\n\n'
        s += f'{message.author.mention} started a roll:'

        newmes = await message.channel.send(s, files=files)
        try:
            await message.delete()
        except discord.Forbidden:
            pass
    
        for x in self.rollemoji:
            await newmes.add_reaction(x)
            await asyncio.sleep(0.02)

    async def lootroll(self, message, member, emoji, me):
        if not member.mention in message.content or message.author.id != me.id:
            return
        if emoji == '🗑️':
            if not message.channel.permissions_for(member).manage_messages:
                await message.delete()
            return
        needgreed = self.rollemoji[:2]
        needers = []
        greeders = []
        for reaction in message.reactions:
            if reaction.emoji not in needgreed:
                continue
            if reaction.emoji == needgreed[0]:
                needers = [user async for user in reaction.users() if not user.bot]
            if reaction.emoji == needgreed[1]:
                greeders = [user async for user in reaction.users() if not user.bot]
        

        if len(needers) > 0:
            rollers = needers
        elif len(greeders) > 0:
            rollers = greeders
        else: return

        rollers = [x.display_name for x in rollers]
        random.shuffle(rollers)
        rolls = sorted(self.generateuniquerolls(len(rollers)), reverse=True)
        s = '```\n'
        s += ' '.join(rollers)
        s += '\n'
        s += ' '.join([f'{rolls[x]: <{len(rollers[x])}}' for x in range(len(rolls))])
        s += '\n```'
        await message.edit(content=f'{message.content}{s}')

    async def reminderjob(self, member, message):
        p = re.compile(r"<t:([0-9]{10}):[R|t|T|d|D|f|F]>")
        timestamp = int(p.findall(message.content)[0])
        then = datetime.fromtimestamp(timestamp)
        now = datetime.now()
        delay = (then - now).seconds

        if delay < -120:
            return
        elif delay > 900:
            await asyncio.sleep(delay-900)
        for x in message.reactions:
            if x.emoji == '☑️':
                users = [user async for user in x.users()] 
                if member in users:
                    await member.send(f"Your gatherable is ready <t:{timestamp}:R> {message.jump_url}")
                break


class OnboardingTicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='Apply for membership', style=discord.ButtonStyle.blurple, custom_id='onboarding_ticket_view:apply')
    async def apply(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Let\'s get you sorted', ephemeral=True)
        await self.handletheresponse(0, interaction)


    @discord.ui.button(label='I am a friend', style=discord.ButtonStyle.green, custom_id='onboarding_ticket_view:friend')
    async def friend(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Welcome, friend', ephemeral=True)
        await self.handletheresponse(1, interaction)
    
    @discord.ui.button(label='Violence', style=discord.ButtonStyle.red, custom_id='onboarding_ticket_view:stabber')
    async def stabber(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('A stabber is upon us', ephemeral=True)
        await self.handletheresponse(2, interaction)

    @discord.ui.button(label='Diplomacy', style=discord.ButtonStyle.grey, custom_id='onboarding_ticket_view:diplomat')
    async def diplomat(self, interaction: discord.Interaction, button: discord.ui.Button):
        mes = await interaction.response.send_message('Let the diplomacy commence', ephemeral=True)
        await self.handletheresponse(3, interaction)

    @discord.ui.button(label='Business', style=discord.ButtonStyle.grey, custom_id='onboarding_ticket_view:customer')
    async def customer(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Straight to business!', ephemeral=True)
        await self.handletheresponse(4, interaction)
    
    async def handletheresponse(self, response, interaction):
        resps = ['Membership', 'Friendship', 'Violence', 'Diplomacy', 'Business']
        chan = interaction.guild.get_channel(1358136176191733932)
        msg = await chan.send(f'{interaction.user.mention} is in the market for: {resps[response]}')
        for x in ['⬆️', '⬇️', '❓']:
            await msg.add_reaction(x)
            await asyncio.sleep(0.02)

# @bot.command()
# async def menu_example(ctx):
#     m = Onboarding()
#     await m.start(ctx)