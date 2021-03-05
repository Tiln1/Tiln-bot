'''
Created on Apr 16, 2018

@author: Tiln
'''
import random
import numpy
from random import randint
import math
import re
from decimal import Decimal
from datetime import datetime, timedelta
import io
import asyncio
import json
import requests
import sys
import string
import justext
import platform
import matplotlib.pyplot as plt
import time
import copy
import sympy # @UnusedImport
from pymongo import MongoClient
import colorsys
from googleapiclient.discovery import build
from PIL import Image
import os
import sounddevice as sd
import pint
#from scipy.io.wavfile import read
#import tts.sapi


import discord
from discord.ext import commands  # @UnresolvedImport @UnusedImport
from discord.ext.commands import Bot  # @UnresolvedImport

from calceval import NumericStringParser  # @UnresolvedImport
from otherStuff import HelpMethods # @UnresolvedImport
# from threading import Thread
# import speech_recognition as sr
# import chessclasses.piececlasses as pc  # @UnresolvedImport
# import chessclasses.algebraicnotation as an  # @UnresolvedImport
# import chessclasses.imagemanipulation as im  # @UnresolvedImport

import tracemalloc
tracemalloc.start()

unit_registry = pint.UnitRegistry()
unit_registry.load_definitions('URUnits.txt')
start_time = time.time()

intent = discord.Intents.default()
intent.members = True
client = Bot(description="General bot", command_prefix="!?", pm_help=False, intents=intent)
client.remove_command('help')


mc = MongoClient('localhost', 27017)
tilndb = mc.tiln
hm = HelpMethods()

asc = ['', '', '', '', '', '', '', '', '    ', '', '', '\n', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ' ', '!', '"', '#', '$', '%', '&', '\'', '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '[', '\\', ']', '^', '_', "`", 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ' ', '¡', '¢', '£', '¤', '¥', '¦', '§', '¨', '©', 'ª', '«', '¬', '­', '®', '¯', '°', '±', '²', '³', '´', 'µ', '¶', '·', '¸', '¹', 'º', '»', '¼', '½', '¾', '¿', 'À', 'Á', 'Â', 'Ã', 'Ä', 'Å', 'Æ', 'Ç', 'È', 'É', 'Ê', 'Ë', 'Ì', 'Í', 'Î', 'Ï', 'Ð', 'Ñ', 'Ò', 'Ó', 'Ô', 'Õ', 'Ö', '×', 'Ø', 'Ù', 'Ú', 'Û', 'Ü', 'Ý', 'Þ', 'ß', 'à', 'á', 'â', 'ã', 'ä', 'å', 'æ', 'ç', 'è', 'é', 'ê', 'ë', 'ì', 'í', 'î', 'ï', 'ð', 'ñ', 'ò', 'ó', 'ô', 'õ', 'ö', '÷', 'ø', 'ù', 'ú', 'û', 'ü', 'ý', 'þ' ]
emojAN = ['🇦', '🇧', '🇨', '🇩', '🇪', '🇫', '🇬', '🇭', '🇮', '🇯', '🇰', '🇱', '🇲', '🇳', '🇴', '🇵', '🇶', '🇷', '🇸', '🇹', '🇺', '🇻', '🇼', '🇽', '🇾', '🇿', '0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']
#:hash: :exclamation: :question: :heavy_plus_sign: :heavy_minus_sign: :heavy_multiplication_x: :heavy_division_sign: :heavy_dollar_sign:
emojmisc = ['#️⃣', '❗', '❓', '➕', '➖', '*⃣', '➗', '💲']
emojdoub = ['🆎', '🆑', '🆔', '🆖', '🆗', '🆚', '🚾', '‼', '⁉', '🆕', '🆘', '🆒', '🆓', '🔟']
cmds = (['reminder', 'cr', 'pchan', 'pchanowned', 'pchancreate', 'annoyingspoilerization', 'singleoption', 'echo', 'invite', 'emojify',
        'setprefix', 'pchansettopic', 'superrps', 'gethexcodes', 'thewave', 'tmfsm', 'morse', 'prune', 'convert', 'createtheroles', 
        'getchannelmembers', 'react', 'cro', 'wordyhelp', 'theoreticalprune', 'wordcount', 'ping', 'reportsfor', 'privatechannels', 
        'trim', 'wiki', 'embedize', 'ctof', 'collectpoll', 'dtm', 'catsays', 'freedom', 'pin', 'customresponses', 'cat', 'search', 'length', 
        'tellbotter', 'pchanrename', 'pfp', 'report', 'rps', 'graph', 'rainbowizetheroles', 'calc', 'disable', 'pchandelete', 'tfsm', 
        'pchankickyourself', 'roll', 'purge', 'rolecount', 'disableablecommands', 'palindrome', 'define', 'echonreturnfirst', 
        'disablelogginghere', 'givereadaccess', 'echonreturnfirstd', 'help', 'listcustomresponses', 'memberrolelist', 'setreportchannel', 
        'clearreactions', 'lcr', 'ftoc', 'np', 'rankedpairs', 'timedroles', 'mountains', 'listroles', 'undisableablecommands', 
        'makeroleamuterole', 'word', 'counting', 'enable', 'haiku'])
udcmds = ['enable', 'disable', 'help', 'wordyhelp', 'freedom', 'disableablecommands', 'undisableablecommands']
link = 'https://discordapp.com/oauth2/authorize?client_id={}&scope=bot%20applications.commands&permissions=285601234'
mes_sage_ids = []
mes_sageid = 0
banned_user = ''
closingflag = False
enrf = {}
to_tilns_channel = [678129794587820052]
countingf = None
haikuf = None
sopf = None
rankedpairsf = None
crf = None
# globboard = None



#:a: :b: :information_source: :pisces: :m: :scorpio: :virgo: :capricorn: :o2: :o: :parking: :Aries: :negative_squared_cross_mark: :x: :grey_exclamation: :grey_question:\

@client.event
async def on_ready():
    print('Logged in as '+client.user.name+' (ID:'+str(client.user.id)+') | Connected to '+str(len(client.guilds))+' guilds | Connected to '+str(len(set(client.get_all_members())))+' users')
    print('--------')
    print('Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__, platform.python_version()))
    print('--------')
    print('Use this link to invite {}:'.format(client.user.name))
    print(link.format(client.user.id))
    print('--------')
    await client.change_presence(activity=discord.Game(name="Invite me! with !?invite"))
    timediff = (time.time() - start_time)
    if timediff < 60:
        global cmds
        cmds = [x.name for x in client.commands]
        cmds = list(set(cmds) - {'wa', 'linkstogames', 'reducemyarray', 'append', 'replace', 'killbot',
            'restartbot', 'aptrentcalc', 'rankedpairsold', 'checktestresults', 'leavevc',
            'editcustomresponseoptions', 'renamealltherolesyesimabsolutelysure', 'givemeeveryrole', 'dm', 'improvedhardening'})
        print(cmds)
        await hm.fourtwenty(client)
        # await hm.autocleanpcdb(client)
    return


@client.event
async def on_message(message):
    global enrf
    rolesset = False
    if not message.guild:
        for x in message.content.split("\n"):
            rp = re.compile(r"\d*d(?:\d|\^|\*|-|\+| )+")
            if x.startswith("!?"):
                await client.process_commands(message)
                return
            elif rp.match(x):
                message.content="!?roll "+x
                cmd = message.content.split(" ", 1)[0][2:]
                await client.process_commands(message)
            else:
                message.content = '!?calc '+x
                await client.process_commands(message)
        message.content = x
        returnids = enrf.get(message.channel.id)
        if returnids and message.content != returnids[2]:
            c = hm.getchannel(hm.getguild(client, returnids[0]), returnids[1])
            await c.send(message.content)
            del enrf[message.channel.id]
        return
    pre = hm.getprefix(str(message.guild.id))
#     if '<@115707766714138627>' in message.content or '<!@115707766714138627>' in message.content:
#         await message.channel.send('Tiln is sleeping')
    if message.content.replace('!', '') == str(client.user.mention):
        await message.channel.send(f'The prefix is `{pre}`.')
    for x in message.content.split("\n"):
        rp = re.compile(r"\d*d(?:\d|\^|\*|-|\+| )+")
        nofree = discord.utils.get(message.guild.roles, name='No Freedom')
        try:
            authroles = message.author.roles
        except:
            authroles = []
        if x.startswith(pre):
            if not rolesset:
                global roles
                roles = message.guild.roles
            rolesset = True
            cmd = x.lower().split(" ", 1)[0][len(pre):]
            message.content = x.replace(pre, '!?', 1)
            if not message.content.startswith('!?customresponses'):
                x = re.sub(r' +', ' ', x)
            donotblock = ['echo', 'calc', 'roll', 'echonreturnfirst', 'reducemyarray']
            if not hm.cmddisabled(str(message.guild.id), cmd):
                if not message.author.bot or cmd in donotblock:
                    await client.process_commands(message)
                    return
            else: await message.channel.send("The command \"" + cmd + "\" is disabled in this guild.")
        elif hm.freedom(str(message.guild.id)) and nofree not in authroles:
                
#             global globboard
#             if globboard and globboard.channel == message.channel.id and globboard.userturn == message.author.id:
# #               try:
# #                 board = copy.deepcopy(globboard)
#                 try:
#                     parsed = an.parse(message.content, globboard, domove=True)
#                 except:
#                     parsed = [False]
# #               globboard = board
#                 msg = await message.channel.fetch_message(globboard.message)
#                 if parsed[0]:
#                     imgboard = im.displayboard(globboard, globboard.turn, parsed[3], parsed[4])
#                     imgboard.save('chessclasses/state.png', format='PNG')
#                     implosion = client.get_user(371801273953026050)
#                     imgondiscord = await implosion.send(file=discord.File('chessclasses/state.png'))
#                     url = imgondiscord.attachments[0].url
#                     embed = discord.Embed(title=parsed[-1])
#                     embed.set_image(url=url)
#                     if globboard.turn == 'B' and globboard.moves() > 0:
#                         globboard.pgn += ' ' + str(globboard.moves() + 1) + '.'
#                     globboard.pgn += ' ' + parsed[1]
#                     
#                     await msg.edit(content=f'{globboard.pgn}', embed=embed)
#                     await message.delete()
#                 elif len(parsed) > 1:
#                     implosion = client.get_user(371801273953026050)
#                     async for x in implosion.history(limit=1):
#                         url = x.attachments[0].url
#                     embed = discord.Embed(title=parsed[-1])
#                     embed.set_image(url=url)
#                     await msg.edit(content=f'{msg.content}', embed=embed)
# #               except: ""
            if rp.match(x) and not hm.cmddisabled(str(message.guild.id), 'roll'):
                message.content = f'{pre}roll '+x
                await client.process_commands(message)
            # ("+" in mc or "-" in mc or "/" in mc or "*" in mc or "^" in mc or "%" in mc or "sin(" in mc or "cos(" in mc or "tan(" in mc or "exp(" in mc or "abs(" in mc or "trunc(" in mc or "round(" in mc or "sqrt(" in mc or "sgn(" in mc or "mod(" in mc or "fact(" in mc) and 
            elif not hm.cmddisabled(str(message.guild.id), 'calc') and message.author.id != 447268676702437376:
                await calc2(message, x)
            
            if not hm.cmddisabled(str(message.guild.id), 'customresponses') and not message.author.bot:
                global crf
                if not crf:
                    servers = tilndb.customresponses.find_one()
                else:
                    servers = crf
                sid = str(message.guild.id)
                server = servers.get(sid) or {}
                if server:
                    '''{mention} {role.mention} {channel.mention} {user.mention}'''
                    
                    'Users are not mentionableable, meaning not gonna use .gettarget, splitting to .getmember and .getrole, and also using .getchannel, of course'
                    user = None
                    role = None
                    channel = None
                    thiscontent = []
                    for y in x.split():
                        user = hm.getmember(message.guild, y, byname=False)
                        if user: continue
                        channel = hm.getchannel(message.guild, y, byname=False)
                        if channel: continue
                        role = hm.getrole(message.guild, y, byname=False)
                        if role: continue
                        thiscontent.append(y)
                    thiscontent = ' '.join(thiscontent)
                    
    
    
                    dminstead = False
                    responses = False
                    readytodelete = False
                    delay = 0
                    for k, v in server.items():
                        selfcontent = thiscontent
                        good = True
                        readytodelete = False
                        dminstead = False
                        delay = 0
                        puncnot = ''.join([x for x in string.punctuation if x not in k])
                        puncin = [x for x in string.punctuation if x in k]
                        selfcontent = selfcontent.translate(str.maketrans('', '', puncnot))
                        if 'ci' in v[0]:
                            k = k.lower()
                            selfcontent = selfcontent.lower()
                        k2 = k
                        sc2 = selfcontent
                        for z in puncin:
                            k2 = k2.replace(z, f' {z} ')
                            sc2 = sc2.replace(z, f' {z} ')
                            
                        perms = {'own': 'message.author != message.guild.owner', '!own': 'message.author == message.guild.owner',
                         'adm': 'not  message.author.guild_permissions.administrator', '!adm': 'message.author.guild_permissions.administrator', 
                         'ms' : 'not message.author.guild_permissions.manage_guild', '!ms' : 'message.author.guild_permissions.manage_guild',
                         'mr' : 'not message.author.guild_permissions.manage_roles', '!mr' : 'message.author.guild_permissions.manage_roles',
                         'mc' : 'not message.author.guild_permissions.manage_channels', '!mc' : 'message.author.guild_permissions.manage_channels',
                         'km' : 'not message.author.guild_permissions.kick_members', '!km' : 'message.author.guild_permissions.kick_members',
                         'bm' : 'not message.author.guild_permissions.ban_members', '!bm' : 'message.author.guild_permissions.ban_members',
                         'mn' : 'not message.author.guild_permissions.manage_nicknames', '!mn' : 'message.author.guild_permissions.manage_nicknames',
                         'mm' : 'not message.author.guild_permissions.manage_messages', '!mm' : 'message.author.guild_permissions.manage_messages',
                         'me' : 'not message.author.guild_permissions.mention_everyone', '!me' : 'message.author.guild_permissions.mention_everyone',
                         'bot' : 'not message.author.bot', '!bot' : 'message.author.bot'}
                        inter = set(perms.keys()) & set(v[0])
                        cont = False
                        for y in inter:
                            if eval(perms[y]):
                                cont = True
                                break
                        if cont: continue
                        for y in v[0]:
                            if y[-1] == '%':
                                num = int(y[:-1])
                                rand = 100*random.random()
                                if num < rand:
                                    good = False
                                    break
                        if not good:
                            continue
                        for y in v[0]:
                            if y[-7:] == 'seconds' and hm.isdigit(y[:-7]):
                                delay = int(y[:-7])
                        if 'd' in v[0]:
                            readytodelete = True
                        if 'dm' in v[0]:
                            dminstead = True
                        if 're' in v[0]:
                            try: result = re.match(k, selfcontent)
                            except: ""
    #                         print(k, x, result)
                            if result:
                                responses = v[1]
                                break 
                        elif 'sss' in v[0]:
                            good = True
                            for y in k2.split():
                                if f'{y}' not in f'{sc2}':
                                    good = False
                            if good:
                                responses = v[1]
                                break
                        elif 'ss' in v[0]:
                            if k in selfcontent:
                                responses = v[1]
                                break
                        elif 'ssw' in v[0]:
                            good = True
                            for y in k2.split():
                                if y in puncin:
                                    if f'{y}' not in f'{sc2}':
                                        good = False
                                        break
                                else:
                                    if f' {y} ' not in f' {sc2} ':
                                        good = False
                                        break
                            if good:
                                responses = v[1]
                                break
                        elif 'sw' in v[0]:
                            if f' {k} ' in f' {selfcontent} ':
                                responses = v[1]
                                break
                        else:
                            if k == selfcontent:
                                responses = v[1]
                                break
                    
                    if responses:
                        try:
                            if readytodelete:
                                await message.delete()
                        except: pass
                        
                        try:
                            response = responses[random.randint(0, len(responses)-1)]
                            if user:
                                response = response.replace('{mention}', user.mention)
                                response = response.replace('{user.mention}', user.mention)
                            if channel:
                                response = response.replace('{mention}', channel.mention)
                                response = response.replace('{channel.mention}', channel.mention)
                            if role:
                                nonerole = False
                                if role.mentionable:
                                    nonerole = True
                                else:
                                    await role.edit(mentionable = True)
                                response = response.replace('{mention}', role.mention)
                                response = response.replace('{role.mention}', role.mention)
                                if nonerole: role = None
                            if delay:
                                await asyncio.sleep(delay*0.25)
                                async with message.channel.typing():
                                    await asyncio.sleep(delay*0.75)
                            if not dminstead:
                                await message.channel.send(response)
                            else:
                                await message.author.send(response)
                            if role:
                                await role.edit(mentionable = False)
                        except: pass
    #                 else: print(message.content)
            if not hm.cmddisabled(str(message.guild.id), 'haiku') and not message.author.id == 447268676702437376:
                global haikuf
                if not haikuf:
                    haikuf = tilndb.words.find_one()

                '''x is the line of text we are dealing with'''
                x = re.sub(r' +', ' ', x)
                cmc = x.split(' ')
                listoflists = [[]]
                good = True
                if len(cmc) > 20:
                    good = False
                if good:
                    for y in cmc:
                        exclude = set(string.punctuation.replace("'", '').replace('-', ''))
                        formword = ''.join(ch for ch in y if ch not in exclude).upper()
                        if formword in haikuf.keys():
                            templistthatgetscopied = []
                            for z in haikuf[formword].split(','):
                                moretemplist = []
                                for w in listoflists:
                                    moretemplist.append(w[:])
                                for w in range(len(moretemplist)):
                                    templist = moretemplist[w][:]
                                    templist.append(f'{z}|{y}')
                                    moretemplist[w] = templist
                                templistthatgetscopied.extend(moretemplist)
                            listoflists = templistthatgetscopied
                        else: 
                            good = False
                            break
                if good:
                    for y in listoflists:
                        total = 0
                        s = ''
                        five = True
                        good = True
                        for z in y:
                            total += int(z.split('|')[0])
                            s += z.split('|')[1] + ' '
                            if ((total == 5 or total == 17) and five) or (not five and total == 12):
                                five = not five
                                s += '\n'
                            if total > 17:
                                good = False
                                break
                        if good and total == 17:
                            lines = s.split("\n")
                            largest = 0
                            for z in lines:
                                largest = len(z) if len(z) > largest else largest
                            for z in range(3):
                                try:
                                    lines[z] = int((largest - len(lines[z]))//2)*' ' + lines[z]
                                except: good = False
                            s = "\n".join(lines)
                            
                            #exemptguilds = [455380663013736479]
                            warning = 'Haiku recognizer'
                            if good:
                                await message.channel.send(f'{warning}\n```{s[:-1]}```')
                            break
            if not hm.cmddisabled(str(message.guild.id), 'palindrome') and not message.author.bot:
                exclude = set(string.punctuation)
                line = ''.join(ch for ch in x if ch not in exclude).lower().replace(' ', '')
                if len(line) > 10:
                    good = True
                    for y in set(line):
                        if y*4 in line:
                            good = False
                            break
                    if good:
                        for y in range(2, len(line)//4+1):
                            for z in range(0, len(line)-y):
                                substr = line[z:z+y]
                                if substr in line.replace(substr, '', 1).replace(substr, '', 1).replace(substr, '', 1):
                                    good = False
                                    break
                    if good:
                        for y, z in zip(line, line[::-1]):
                            if not y == z:
                                good = False
                            if not good:
                                break
                    if good:
                        await message.channel.send(f'Palindrome recognizer\n```\n{x[::-1]}```')
            if not hm.cmddisabled(str(message.guild.id), 'someone') and not message.author.bot and '@someone' in f' {x} ':
                if message.channel.permissions_for(message.author).mention_everyone:
                    mems = message.channel.members
                    mems.remove(message.author)
                    await message.channel.send(x.replace('@someone', mems[random.SystemRandom().randint(0, (len(mems)-1))].mention))
                    if '\n' not in message.content:
                        await message.delete()
    



    if message.channel.id == 455380663013736481 and not message.author.bot:
        embed = discord.Embed(description=message.content, url=message.jump_url, color=message.author.color)
        embed.set_author(name=message.author.name, icon_url=message.author.avatar_url)
        await client.get_channel(798796210491228160).send(embed=embed)
        # await client.get_channel(798796210491228160).send(s)
    elif message.channel.id == 798796210491228160 and not message.author.bot:
        await client.get_channel(455380663013736481).send(message.content)

    global to_tilns_channel
    exclude = set(string.punctuation)
    conexpun = ''.join(ch for ch in message.content if ch not in exclude).lower()
    if message.channel.id == to_tilns_channel[0] and not message.author.bot and len(to_tilns_channel) > 1:
        if message.author.id == 115707766714138627:
            to_tilns_channel = [678129794587820052]
            return
        files = []
        for y in message.attachments:
            y = await y.to_file()
            files.append(y)
        await client.get_channel(678129794587820052).send(message.author.mention + ': ' + message.content, files=files)
        return
    elif message.channel.id == 678129794587820052 and (message.content.lower() == 'stop' or message.content.startswith('!?')):
        to_tilns_channel = [678129794587820052]
        return
    elif message.channel.id == 678129794587820052 and not message.author.bot and len(to_tilns_channel) > 1:
        if '\n' not in message.content:
            con = f'Tiln: {message.content}'
        else:
            con2 = ' '*8 + message.content.replace('\n', '\n        ')
            con = f'Tiln: \n{con2}'
        await client.get_channel(to_tilns_channel[0]).send(con)
        return
    elif ' tiln ' in f' {conexpun} ' and not message.author.bot and message.author.id != 115707766714138627:
        to_tilns_channel = [message.channel.id, to_tilns_channel[0]]
        chan = f'<#{message.channel.id}>' if client.get_user(115707766714138627) in message.channel.members else message.channel.name
        s = f'Tiln, {message.author.mention} said your name in {chan}:\n'
        files = []
        for y in message.attachments:
            y = await y.to_file()
            files.append(y)
        await client.get_channel(678129794587820052).send(s + message.content, files=files)
        return

    
    
    
    returnids = enrf.get(message.channel.id)
    if returnids and message.content != returnids[2]:
        c = hm.getchannel(hm.getguild(client, returnids[0]), returnids[1])
        await c.send(message.content)
        del enrf[message.channel.id]
        return
    
    global countingf
    if not countingf:
        countingf = tilndb.counting.find_one()
    #load dictionary
    gid = str(message.guild.id)
    gc = countingf.get(gid) or {}
    cid = str(message.channel.id)
    chanc = gc.get(cid) or {}
    #store in dictionary
    if chanc and chanc.get('inc') != 'off':
        cur = chanc.get('current')
        if message.content != cur:
            try:
                await message.delete()
            except: ""
            return
        
        num = int(message.content)
        reactions = []
        reactionables = {"message.content == message.content[::-1]": ['🇵','🇦','🇱','🇮','🇳','🇩','🇷','🇴','🇲','🇪'], 
                         "num == int(num**0.5)**2": hm.numtoreactions(int(num**0.5)) + ['🇸', '🇶', '🇺', discord.utils.get(client.emojis, name="a_", id=448623554292875266), '🇷', discord.utils.get(client.emojis, name="e_", id=448623554582282260), discord.utils.get(client.emojis, name="d_", id=448623287782604801)],
                         "sympy.isprime(num)": ['🇵', '🇷', '🇮', '🇲', '🇪'],
                         }
        for k, v in reactionables.items():
            if eval(k.replace('__', '')):
                if len(reactions):
                    reactions.append('➕')
                reactions += v
        if len(reactions):
            reactions.append('🎉')
        inc = chanc.get('inc').replace('^', '**')
        chanc.update({'current':str(eval(cur + inc))})
        gc.update({cid:chanc})
        countingf.update({gid:gc})
        #write to file
        tilndb.counting.replace_one({}, countingf)
        for y in reactions:
            await message.add_reaction(y)
                
        
            
            
# @client.event
# async def on_member_update(before, after):
#     if before.roles == after.roles:
#         return
#     sid = after.guild.id
#     
#     file = open('jsons/exclusiveroles.json', 'r+')
#     exguilds = json.load(file)
#     exrg = exguilds.get(str(sid))
#     
#     linkrp = json.load(open('jsons/linkedroles.json', 'r+')).get(str(sid))
#     #role added
#     try:
#         for x in after.roles:
#             if linkrp:
#                 for y in linkrp:
#                     if x.name == y.split(':')[0] and not x in before.roles:
#                         await after.add_roles(discord.utils.get(after.guild.roles, name=y.split(":")[1]), atomic=False)
#             if exrg:
#                 for y in exrg:
#                     if x.name in y.split(':') and not x in before.roles:
#                         rtr = []
#                         for z in y.split(':'):
#                             if not z == x.name:
#                                 rtr.append(discord.utils.get(after.guild.roles, name=z))
#                         await after.remove_roles(*rtr, atomic=False)
#     
#         
#                     
#         #role removed
#         for x in before.roles:
#             if linkrp:
#                 for y in linkrp:
#                     if x.name == y.split(':')[0] and not x in after.roles:
#                         await after.remove_roles(discord.utils.get(after.guild.roles, name=y.split(":")[1]), atomic=False)
#     except: ""

@client.event
async def on_message_delete(message):
    if not message.guild:
        return
    if message.channel.name == 'deletion-log':
        return
    servers = tilndb.deloggedchannels.find_one()
    gid = str(message.guild.id)
    channelids = servers.get(gid) or []
    if message.channel.id in channelids:
        return
    await asyncio.sleep(0.05)
    try:
        if message.id in mes_sage_ids:
            return
    except: ""
    attachments = message.attachments
    content = f'content:\n\\{message.content}' if message.content else 'no content.'
    author = message.author
    guild = message.guild
    
    Abot = f'A bot or {author}'
    #message.guild.fetch_member(447268676702437376)
    deleter = 'I' if mes_sageid == message.id else Abot
    if deleter == Abot:
        for _11 in range(2):
            try:
                async for x in guild.audit_logs(limit=10, action=discord.AuditLogAction.message_delete):
                    if x.target == author:
                        deleter = x.user
                if str(deleter) != Abot:
                    break
                await asyncio.sleep(0.1)
            except discord.errors.Forbidden:
                Abot = '[Cannot view the audit log to set deleter]'
                deleter = Abot
    if deleter == 'I':
        Abot = 'I'
    dname = str(deleter)
    dmen = ''
    if str(deleter) != Abot:
        dmen = deleter.mention
    
    for x in guild.text_channels:
        if x.name == 'deletion-log':
            dmen = '' if deleter in x.members else f'({dmen})'
            mention = '' if author in x.members else f'({author.mention})'
            s = f'{author}\n{dname}{dmen} deleted a message by {author}{mention} in {message.channel.mention} with {content}'
            files = []
            if attachments:
                s += '\nAnd attachment(s):'
                ats = len(attachments)
                for y in range(ats):
                    at = attachments[y]
                    byts = requests.get(at.proxy_url).content
                    file = io.BytesIO(byts)
                    file.name = at.filename
                    files.append(discord.File(file))
            await x.send(s[:2000], files=files)
                 
            

@client.event
async def on_raw_bulk_message_delete(payload):
    mes_sage_ids.extend(payload.message_ids)
    await asyncio.sleep(20)
    for x in payload.message_ids:
        mes_sage_ids.remove(x)


@client.event
async def on_message_edit(before, after):
    if before.content == after.content or not before.guild or before.author.bot:
        return
    servers = tilndb.deloggedchannels.find_one()
    gid = str(after.guild.id)
    channelids = servers.get(gid) or []
    if after.channel.id in channelids:
        return
    beforre = before.content.replace("\n", "\\n")
    afterr = after.content.replace("\n", "\\n")
    guild = after.guild
    editor = after.author
    desc = f'message edited in {after.channel.mention}'
    for x in guild.text_channels:
        if x.name == 'deletion-log' or x.name == 'edit-log':
            mention = '' if editor in x.members else f'({editor.mention})'
            n = '\n\n' if len(beforre) > 60 else '\n'
            await x.send(f'{desc} by {str(editor)}{mention}\n**Before:** {beforre}{n}**After:** {afterr}'[:2000])
    
@client.event
async def on_member_join(member):
    guild = member.guild
    if not hm.getmember(guild, '447268676702437376').guild_permissions.manage_roles:
        return
    await asyncio.sleep(5)
    servers = tilndb.rolepersistance.find_one()
    gid = str(member.guild.id)
    persistedusers = servers.get(gid) or {}
    mid = str(member.id)
    persistedroles = persistedusers.get(mid) or []
    roles = []
    for x in persistedroles:
        roles.append(discord.utils.get(member.guild.roles, id=x))
    try:
        roles.remove(discord.utils.get(member.guild.roles, name='@everyone'))
    except: pass
    prevroles = None
    if roles:
        memroles = member.roles
        del memroles[0]
        if memroles != roles:
            try:
                prevroles = member.roles
                try:
                    roles.remove(discord.utils.get(member.guild.roles, name='@everyone'))
                except: pass
                await member.remove_roles(*member.roles, atomic=False)
            except: ""
            await asyncio.sleep(1)
            roles2 = copy.copy(roles)
            await member.add_roles(*roles, atomic=False)
        else: return
        if guild == client.get_guild(455380663013736479):
            guild.get_channel(563076821747367936).send(f'Restored {[x.name for x in roles2]} to {member.mention} upon their rejoining and removed {[x.name for x in prevroles]}')
        persistedusers.pop(mid, None)
        servers.update({gid: persistedusers})
        tilndb.rolepersistance.replace_one({}, servers)
        
#     else:
#         if guild == client.get_guild(455380663013736479): 
#             guild.get_channel(460290595907305482).send(f'Hey {member.mention}, welcome to **Egg, Inc.**\nPlease see <#455385905499340813>, #455403745899970560, and <#455396915731890177> to get started. Check out <#455393263575236628> and post a screenshot of your prestige screen in #<455385874788777994> to get access to many more channels, including the ones where you can look for coops to join.\nThank you.')
        
    
@client.event
async def on_member_remove(member):
    await asyncio.sleep(.5)
    if member == banned_user or not hm.getmember(member.guild, '447268676702437376').guild_permissions.manage_roles:
        return
    servers = tilndb.rolepersistance.find_one()
    gid = str(member.guild.id)
    persistedusers = servers.get(gid) or {}
    mid = str(member.id)
    persistedroles = []
    for x in member.roles:
        if x.name != '@everyone':
            persistedroles.append(x.id)
    persistedusers.update({mid: persistedroles})
    servers.update({gid: persistedusers})
    tilndb.rolepersistance.replace_one({}, servers)
    
# @client.event
# async def on_member_ban(guild, user):
#     banned_user = user
    
@client.event
async def on_raw_reaction_add(payload):
    if payload.user_id == 447268676702437376:
        return
    global rankedpairsf
    guild = client.get_guild(payload.guild_id)
    emoji = payload.emoji
    if guild:
        chan = guild.get_channel(payload.channel_id)
        member = guild.get_member(payload.user_id)
        try: message = await chan.get_message(payload.message_id)
        except: return
        
        sing = True
        if hm.getmember(member.guild, '447268676702437376').guild_permissions.manage_messages and hm.getmember(member.guild, '447268676702437376') != member:
            global sopf
            if not sopf:
                sopf = tilndb.singleoptionpolls.find_one()
            try:
                single = sopf.get(str(payload.guild_id)).get(str(payload.channel_id)).get(str(payload.message_id))
            except: sing = False
            if not sing or not single: sing = False
            if sing:
                for x in message.reactions:
                    if x.emoji == str(emoji):
                        continue
                    if type(x.emoji) != str:
                        if x.emoji.name == emoji.name:
                            continue
                    users = await x.users().flatten()
                    if member in users:
                        await x.remove(member)
                        continue
        
        if not rankedpairsf:
            rankedpairsf = tilndb.rankedpairs.find_one()
        rankedpairs = rankedpairsf.get(str(message.id))
        if not rankedpairs:
            return
        responses = rankedpairs.get('responses')
        options = copy.copy(rankedpairs.get('options'))
        emojis = copy.copy(rankedpairs.get('emoji'))
        option = options[emojis.index(emoji)]
        responses.update({str(member.id): [option]})
        rankedpairs.update({'responses': responses})
        options.remove(option)
        emojis.remove(emoji)
        
        polltitle = rankedpairs.get('polltitle')
        s = f'Pick your 2nd choice, or :no_entry_sign: to be done. All unranked options are tied and below the ranked ones. Please react with the :no_entry_sign: when you are done.\n{polltitle}'
        s += hm.makeRPpoll(options, emojis)[0]
        messagesent = await member.send(s)
        for x in emojis + ['🚫']:
            await messagesent.add_reaction(x)
        
        await message.remove_reaction(emoji, member)
        rankedpairsf.update({str(message.id): rankedpairs, str(member.id): {'master': message.id, 'this': messagesent.id}})
        tilndb.rankedpairs.replace_one({}, rankedpairsf)
    else:
        user = await client.fetch_user(payload.user_id)
        message = await user.fetch_message(payload.message_id)
        if not rankedpairsf:
            rankedpairsf = tilndb.rankedpairs.find_one()
        storeduser = rankedpairsf.get(str(user.id))
        rpmessageid = storeduser.get('master')
        if not rpmessageid or storeduser.get('this') != message.id:
            return
        rankedpairs = rankedpairsf.get(str(rpmessageid))
        responses = rankedpairs.get('responses')
        options = copy.copy(rankedpairs.get('options'))
        emojis = copy.copy(rankedpairs.get('emoji'))
        optionssofar = responses.get(str(user.id))
        
        if emoji != '🚫':
            option = options[emojis.index(emoji)]
            optionssofar.append(option)
            responses.update({str(user.id): optionssofar})
            rankedpairs.update({'responses': responses})
        if len(optionssofar) != len(options) and emoji != '🚫':
            for x in optionssofar:
                ind = options.index(x)
                options.remove(x)
                emojis.pop(ind)
            polltitle = rankedpairs.get('polltitle')
            s = f'Pick your {hm.rankednum(len(optionssofar)+1)} choice, or :no_entry_sign: to be done. All unranked options are tied and below the ranked ones. Please react with the :no_entry_sign: when you are done.\n{polltitle}'
            s += hm.makeRPpoll(options, emojis)[0]
            messagesent = await user.send(s)
            for x in emojis + ['🚫']:
                await messagesent.add_reaction(x)
            await message.delete()
            rankedpairsf.update({str(rpmessageid): rankedpairs, str(user.id): {'master': rpmessageid, 'this': messagesent.id}})
        else:
            await message.delete()
            del rankedpairsf[str(user.id)]
            rankedpairsf.update({str(rpmessageid): rankedpairs})
            s = 'React to the original poll if you would like to redo your votes.\n```'
            for idx, x in enumerate(responses.get(str(user.id))):
                s += f'\n{hm.rankednum(idx+1)} {x}'
            for x in [y for y in options if y not in responses.get(str(user.id))]:
                s += f'\n{hm.rankednum(len(options))} {x}'
            await user.send(s + '```')
        
        tilndb.rankedpairs.replace_one({}, rankedpairsf)
        
        
# @client.event
# async def on_guild_channel_update(before, after):
#     if before.position != after.position and before.guild.id == 455380663013736479:
#         await hm.getchannel(before.guild, 679551603782451319).send(f'{before.name} moved from {before.position} to {after.position}')
#             
# @client.event
# async def on_raw_reaction_add(payload):
#     guild = client.get_guild(payload.guild_id)
#     chan = guild.get_channel(payload.channel_id)
#     member = guild.fetch_member(payload.user_id)
#     message = chan.fetch_message(payload.message_id)
    
@client.command()
async def np(ctx):
    msg = await ctx.channel.send("Pong!")
    time = math.trunc((msg.created_at - ctx.message.created_at).total_seconds() * 1000)
    if time > 0:
        await msg.delete()
        try:
            await ctx.message.delete()
        except: pass
    else:
        await msg.edit(content="Pong! `" + str(time) + " ms`")

@client.command()
async def ping(ctx):
    if str(ctx.author) == "Tiln#0416":
        #msg = ctx.message
        #msg.id = int('1' + len(str(ctx.author.id))*'0')
        #print(msg.created_at)
        if 'leave' in ctx.message.content:
            await ctx.guild.leave()
        else:
            await ctx.send('Connected to '+str(len(client.guilds))+' guilds')
#         ent = await ctx.guild.audit_logs().flatten()
#         for idx, x in enumerate(ent):
#             if idx > 20: break
#             print(x)
#         cmc = ctx.message.content.split()[1:]
#         mes = await ctx.channel.fetch_message(int(cmc[0]))
#         embed = embed=discord.Embed(title=f'Hi, I\'m a title for this post from {mes.author.name}', description=mes.content+f'\n\n{mes.jump_url}',  timestamp=mes.created_at, url=mes.jump_url)
#         embed.set_footer(text='Hi, I\'m an unused footer')
#         embed.set_author(name=mes.author.name, icon_url=mes.author.avatar_url)
#         await ctx.send(embed=embed)
#         print(ctx.guild.premium_subscribers)
#         await ctx.send([x.name for x in ctx.guild.premium_subscribers])
        # for x in ctx.guild.members:
        #     if x.activity != None and x.activity.type != 4 and str(x.activity.type) == "ActivityType.streaming":
        #         print(x.name, x.activity, x.activity.url)
#         for x in sorted(client.guilds, key=lambda x: x.member_count, reverse=True):
#             print(f'{x.name}: {x.member_count}')

#         msg = await ctx.channel.fetch_message(int(ctx.message.content.split(" ")[1]))
#         for x in msg.reactions:
#             async for y in x.users():
#                 print(str(x.emoji) + ": " + y.name + '#' +  y.discriminator)
    else:
        msg = await ctx.channel.send("Pong!")
        time = math.trunc((msg.created_at - ctx.message.created_at).total_seconds() * 1000)
        await msg.edit(content="Pong! `" + str(time) + " ms`")
    
    
    
@client.command()
async def help(ctx):
    com = ctx.message.content.lower().split(" ")
    try:
        pre = hm.getprefix(str(ctx.guild.id))
    except: pre = '!?'
    base = False
    if len(com)>1:
        c = com[1]
        if not hm.cmddisabled(str(ctx.guild.id), c):
            helpdict = ({"disable": "*commandstodisable\n"+pre+"disable command1 command2 command3",
                "enable": "*commandstoenable\n"+pre+"enable all",
                "pin": "",
                "clearreactions": "<@member/messageid/number of messages>\n<> Means optional\n",
                "roll": "<<number of dice>d[how large of a dice][plus or minus some number to add to each roll]> <something to do to the total>\nExample: "+pre+""+c+" 5d6+1 +1",
                "rps": "[Rock/Paper/Scissors]",
                "purge": f"<messages to purge>(or 1) <roles/members to specifically target to delete> !<roles/members to specifically target to not delete>\norder does not matter with these arguments at all.",
                "collectpoll": "channelid [number of messages that consist of the poll]",
                "reminder": "*[time][y/o/w/d/h/m/s] Reason for timer\n"+pre+""+c+" 1y It has been a year haha!",
                "timedroles": "[time][y/o/w/d/h/m/s] role_name\n"+pre+""+c+" 1y the_best_role",
                "privatechannels": "[enable or disable or [maximum amount of free creation channels] or category(by id or name) or role(by mention, name, or id)]\nor "+pre+""+c+" [owner(by mention, full name, or id)] [channel(by id, name, or mention)] <category(by id or name)>\n<> means optional.",
                "pchan": "[invite or kick or setspectator or setlistener or transferownership] target(role or member(by id, mention or (full)name)) channel(by id, mention, or name)\n",
                "pchancreate": "channelname <category(by name or id)> <file here if you want voice instead>\n",
                "pchandelete": "channel(by id, mention or name)\n",
                "pchanowned": "",#done
                "emojify": "[message]",
                "pfp": "<member reference>",
                "rolecount": "rolecount *roles",
                "dtm": "messageid <channelid or channelmention>(if outside sent channel)",
                "calc": "calc expression",
                "palindrome": "palindrome message",
                "morse": "morse message or morse text",
                "wordcount": "wordcount target(by id, mention or name+discriminator)",
                "prune": f"prune days [targets to protect] *![targets to unprotect]",
                "convert": f"`base1 base2 [number to convert]",
                "report": f"member reason",
                "reportsfor": f"member",
                "setreportchannel": f"[channel]",
                "echo": f"<channel to echo to> [echo content]",
                "customresponses": f"<options,(use{pre}cro for options and descriptions)>",
                "rainbowizetheroles": f"[Starting Role] [Range of Colors(as in 30-300)] [Number of roles] <reverse>",
                "rankedpairs": f'<channel> [title] [*poll options], example: {pre}rankedpairs "Example poll" "option 1" "option 2" "option 3"',
                "wiki":"[search term/number] {search term}",
                "ping":"",#done
                "freedom":"",#done
                "disableablecommands":"",#done
                "cro":"",#done
                "np":"",#done
                "ftoc":"[degrees]",
                "tellbotter":"[message]",
                "memberrolelist":"[role]",
                "echonreturnfirstd":"[guild id] [channel id/user name, role, or id] [message]",
                "ctof":"[degrees]",
                "pchansettopic":"{channel id/name} [topic]",
                "undisableablecommands":"",#done
                "trim":"[string]",
                "getchannelmembers":"{channel id/name}",
                "counting":"",
                "embedize":"",
                "thewave":"",
                "cat":"",#done
                "echonreturnfirst":"[guild id] [channel id/user name, role, or id] [message]",
                "listcustomresponses":"",
                "createtheroles":"",
                "word":"",
                "react":"",
                "tfsm":"",
                "theoreticalprune":"",
                "annoyingspoilerization":"[text]",
                "pchanrename":"",
                "search":"",
                "gethexcodes":"",
                "catsays":"[text]",
                "tmfsm":"",
                "define":"[word]",
                "help":"",
                "makeroleamuterole":"",
                "cr":"",
                "length":"",
                "wordyhelp":"",#done
                "listroles":"",#done
                "setprefix":"[prefix]",
                "pchankickyourself":"",
                "disablelogginghere":"",
                "invite":"",
                "lcr":"",
                "givereadaccess":"",
                "superrps":"[text]",
                "mountains":"",
                "singleoption":"",
                "graph":""#done
                })
            
            if c == "react":
                if len(com) > 2:
                    b = com[2]
                    if b == "repeats":
                        await ctx.channel.send("```diff\n3 on all letters;\n-j, k, q, z\n+a, a, d, e, e, h, i, i, l, m, n, o, r, s, t, t, !, ?, *, *```")
                        return
                    elif b == "doubles":
                        await ctx.channel.send("```ab, cl, id, ng, ok, vs, wc, !!, "+pre+", new, sos, cool, free, 10```")
                        return
                    elif b == "misc":
                        await ctx.channel.send("```+, -, *, /, $, !, ?```")
                    return
                await ctx.channel.send("```"+pre+""+c+" <@member/messageid> *reactions\n<> Means optional and skippable```")
                return
            await ctx.channel.send(f'{pre}{c} {helpdict.get(c)}' if helpdict.get(c) else f"{pre}{c} is not currently a command")
        else: await ctx.channel.send(""+pre+""+c+" is disabled")
    else: base = True
    s = "A.K.A Syntactic Help\n"
    if base:
        s += "```"+pre+"help Displays this command\n"+pre+"collectpoll collects a poll\n"+pre+"rolecount counts the number of people in the specified role(s)\n"+pre+"pchan "+pre+"pchancreate "+pre+"pchandelete "+pre+"pchanowned Does private channels things\n"
        if ctx.channel.permissions_for(ctx.author).manage_guild:
            s += ""+pre+"enable enables commands\n"+pre+"disable disables commands\n"+pre+"setprefix changes the bot prefix"
            if ctx.channel.permissions_for(ctx.author).manage_channels:
                s += ""+pre+"privatechannels does private channels things\n"
        if ctx.channel.permissions_for(ctx.author).add_reactions and ctx.channel.permissions_for(discord.utils.get(ctx.guild.members, id=447268676702437376)).add_reactions:
            s += ""+pre+"react adds reactions to the most recent message\n"
        if ctx.channel.permissions_for(ctx.author).manage_roles and ctx.channel.permissions_for(discord.utils.get(ctx.guild.members, id=447268676702437376)).manage_roles:
            s += ""+pre+"uroles adds and or removes role(s) from a member\n"+pre+"timedroles adds roles based on their time in the guild\n"
        if ctx.channel.permissions_for(ctx.author).manage_messages and ctx.channel.permissions_for(discord.utils.get(ctx.guild.members, id=447268676702437376)).manage_messages:
            s += ""+pre+"purge purges the most recent n messages or n messages by a specified user checking only the most 100 recent messages\n"+pre+"pin pins the most recent message\n"+pre+"clearreactions clears the reactions of the most recent message\n"
        s += ""+pre+"help [command] for help on that command```"
        await ctx.channel.send(s)
        

@client.command()
async def wordyhelp(ctx):
    cmc = ctx.message.content.lower().split(" ")[1:]
    pre = '!?'
    if ctx.guild:
        pre = hm.getprefix(str(ctx.guild.id))
    
    shd = ({"wordyhelp": "You are currently using the `wordyhelp` command. Use `wordyhelp [command]` for superhelp on that command. ` ` is the default [and currently only] argument separator.\n```",  
          "disable": "`disable` disables a currently enabled command. Simply specify the commands you wish to disable as arguments to disable them. `all` can also be given as an argument to `disable`. All commands are enabled by default. Requires the manage server permission.",
          "enable": "`enable` enables commands. Simply specify the commands you wish to enable as arguments to enable them. `all` can also be given as an argument to `enable`. All commands are enabled by default. Requires the manage server permission.",
          "help": "`help` gives more simplistic help on commands, specific syntax and short descriptions. Give the command name as an argument to `help` for help on that command.",
          "pin": "`pin` pins a message, either the latest message, a message specified by id, or a user by mention as the first argument to `pin`.",
          "ping": "`ping` returns a (usually) inaccurate round trip time from you to the bot in milliseconds.",
          "react": "`react` reacts to a message. Emoji, letters, and numbers are all specifiable. The message can be specified by message id or by mentioning the user you want to react to as the first argument to the command. Otherwise/where applicable, reacts to the latest message.",
          "clearreactions": "`clearreactions` clears the reactions off a message. The message can be specified by message id or by mentioning the user you want to react to as the first argument to the command. Otherwise/where applicable, clears from the latest message with reactions. Requires the manage messages permission.",
          "purge": "`purge` purges a number of messages specified by a number anywhere. Targets can be specified as deletable or protected by specifying them or specifying them with any character at the beginning or end, respectively. Requires the manage messages permission.",
          "collectpoll": "`collectpoll` collects a poll from a specified channel. If a poll consists of multiple messages, or you want to collect multiple polls at the same time, a number may be specified. args are: channelid (pointing out the poll location), poll-length (a number), roles and/or users followed by a number as a vote multiplier (must be specified after poll-length), and 'before' followed by a messageid if you want to exclude anyone that joined after that message.",
          "reminder": "`reminder` reminds the command sender after a certain amount of time specified in the first argument (example: 32d4h50s) with an optional reason specified as the second argument.",
          "timedroles": "`timedroles` assigns the specified roles to everyone that has been in the guild for at least the specified time. That time is given as the first argument (exam: 500s) and then the roles you wish to assign are specified as further arguments (by name with '_' in place of spaces). Requires the manage roles permission.",
          "privatechannels": "`privatechannels` allows the addition of users as owners of channels, created with the command or not. It can also allow or deny freecreation, give roles the ability to create channels or not, set categories to be able to have channels created in them or not, and set the maximum number of freecreations.  Requires the manage guild and manage channels permissions.",
          "pchan": "`pchan` allows you to manage the members and roles of channels you own. It takes any one of [invite, kick, superkick, setspectator, setlistener] as the first argument. The intended target (role or member (by id, mention or (full)name)) as the second argument. And the intended channel (by id, mention, or name) as the third argument (unless you're in the target channel).",
          "pchancreate": "`pchancreate` allows a user to create a private channel, with name as the first argument, desired category as the second argument, and any value present as a third argument to set it as voice. Arguments may contain spaces.",
          "pchanowned": "`pchanowned` returns the channels you own in that guild.",
          "pchanrename": "`pchanrename` renames the specified channel to the specified name. Channels can be specified by id, name, or by being in that channel. Argument order doesn't matter.",
          "pchansettopic": "`pchansettopic` changes the topic of the specified channel to the specified topic. Channels can be specified by id, name, or by being in that channel. Argument order doesn't matter.",
          "setprefix": "`setprefix` changes the prefix the bot uses in that server. Can contain spaces. Requires the manage server permission.",
          "report": "`report` reports a user. Requires a member and a reason.",
          "reportsfor": "`reportsfor` retreives the reports for a user. Requires some moderator permissions to utilize.",
          "setreportchannel": "`setreportchannel` toggles a channel where reports are sent. Requires some moderator permissions to utilize.",
          "define": "`define` defines the given [english] word provided.",
          "roll": "`roll` rolls the specified number of the specified sided dice. `20d20+1 +1` for example would roll 20 d20s and then add 1 to each result then add 1 to the total.",
          "rps": "`rps`, or rock paper scissors allows you to play rock paper scissors, but you can use any word besides just the three if you want!",
          "emojify": "`emojify` emojifies the argument and deletes the command invocation message.",
          "pfp": "`pfp`, or profile-pic returns the pfp of the target or yourself.",
          "rolecount": "`rolecount` returns the number of people that have the specified role(s). The role you wish to count is given as the second argument.",
          "calc": "`calc` is a fairly basic calculator for math. The command does not need to be specified in this case, for convenience.",
          "palindrome": "`palindrome` tells you if the given argument is a palindrome.",
          "dtm": "`dtm`, or direct to message, takes a message id and an optional channel id and returns a link to that message.",
          "morse": "`morse` returns the morse version of the given argument or the english version of the given morse-only argument.",
          "invite": "`invite` returns an invite link for `!?`, the bot!",
          "wordcount": "`wordcount` returns the number of words in this channel sent by users after and/or before any number of specified messages.",
          "counting": "`counting` sets the specified channel to a counting only channel, set with a specifiable increment, start, and increment type. Requires manage server permission.",
          "word": "`word` returns the syllable count of the given word, or assigns a syllable count to a word.",
          "freedom": "`freedom` enables features that are triggered by a means that's not a comannd. Requires manage guild permission.",
          "convert": "`convert` converts numbers from one base to another. The first argument should be the base you are converting from, the second the base which you are converting to, and the third the number you wish to convert.",
          "prune": "`prune` prunes a guild by kicking all members that have been inactive for the specified time. Any roles or members can be specified to be protected from pruning. Requires manage guild and kick members permissions.",
          "theoreticalprune": "`prune`, but without the kicking.",
          "echo": "`echo` repeats what you say, a reference to a channel can be put in anywhere to post it to that channel, line breaks can be inserted with \\n",
          "tellbotter": "Tells the creator of the bot something.",
          "wiki":"`wiki` searches Wikipedia for a given query. The first argument can either be the query, or a number specifying the amount of results you wish to see. If a number is given, the query is the second argument.",
          "pchandelete":"`pchandelete` deletes the specified pchan, the name of the pchan is given as the first argument to the command.",
          "disableablecommands":"`disableablecommands` returns a list of the bot's commands which you can disable. Requires manage_server permission.",
          "cro":"`cro` returns a list of custom response options, takes no arguments. Requires manage_messages permission.",
          "np":"`np` will give a response if the ping time between you and the bot turns out negative somehow, otherwise it will delete the invocation message.",
          "ftoc":"`ftoc` converts the given number from degrees Fahrenheit to degrees Celsius.",
          "memberrolelist":"`memberrolelist` gets a list of the members who have the supplied role, can accept multiple roles.",
          "echonreturnfirstd":"`echonreturnfirstd` will echo a message in another server's channel and will give you the response, deletes the command usage.",
          "ctof":"`ctof` converts the given number from degrees celsius to degrees Fahrenheit.",
          "undisableablecommands":"`undisableablecommands` returns a list of the bot's commands which you cannot disable.",
          "trim":"`trim` removes all spaces in the string",
          "getchannelmembers":"`getchannelmembers` returns a list of the members in the specified channel, if no channel is given it will use the channel which you are currently in.",
          "embedize":"",
          "thewave":"",
          "cat":"`cat` will show you a picture of a nice cat.",
          "echonreturnfirst":"`echonreturnfirst` will echo a message in another server's channel and will give you the response.",
          "listcustomresponses":"`listcustomresponses` returns a list of the custom responses which you have created.",
          "createtheroles":"",
          "customresponses":"",
          "tfsm":"",
          "rainbowizetheroles":"",
          "annoyingspoilerization":"`annoyingspoilerization` takes the given text and makes each character a spoiler",
          "search":"`search` searches Google for a given query. The first argument can either be the query, or a number specifying the amount of results you wish to see. If a number is given, the query is the second argument.",
          "gethexcodes":"",
          "catsays":"`catsays` sends a random picture of cat with the given text on it",
          "tmfsm":"",
          "makeroleamuterole":"`makeroleamuterole` turns the specified role mute. The role is specified as the first argument by name, id, or mention.",
          "cr":"",
          "length":"",
          "listroles":"`listroles` returns a list of roles in the current guild.",
          "rankedpairs":"",
          "pchankickyourself":"`pchankickyourself` does what it says on the tin, and kicks you from a specified private channel.",
          "disablelogginghere":"",
          "lcr":"",
          "givereadaccess":"",
          "superrps":"`superrps` basically like regular rock paper scissors, but uses a huge variety of words and accepts any string for your input.",
          "mountains":"",
          "singleoption":"",
          "graph":"`graph` creates a graph of the roles and member count for each role in the server",
          })
    s = ""
    if not cmc:
        s = shd.get('wordyhelp')
        for x in sorted(cmds):
            s += x + (22-len(x))*' '
        s = s[:-1][:1997] + "```"
        await ctx.channel.send(s)
        return
    for x in cmc:
        s += "```" if len(cmc) > 1 else ""
        s += shd.get(x) or x + " is not a command as far as I am aware."
        s += "``` " if len(cmc) > 1 else ""
    await ctx.channel.send(s[:2000])
    

@client.command()
async def disable(ctx):
    if await hm.noperms(ctx, 'manage_guild'):
        return
    if await hm.helpredirect(ctx, client): return
    servers = hm.cmds()
    sid = str(ctx.guild.id)
    server = servers.get(sid) or []
    
    cmc = ctx.message.content.split(" ")[1:]
    if len(cmc) > 0:
        for x in cmc:
            if x in list(set(cmds).difference(udcmds)):
                disableable = True
                for y in server:
                    if y == x:
                        disableable = False
                        break
                if disableable:
                    server.append(x)
            elif x == "all":
                for y in list(set(cmds).difference(udcmds)):
                    disableable = True
                    for z in server:
                        if z == y:
                            disableable = False
                            break
                    if disableable:
                        server.append(y)
                break
    else: return
    servers.update({sid:server})
    hm.updatecmds(servers)
    await ctx.channel.send("Success")
    
@client.command()
async def disableablecommands(ctx):
    if await hm.noperms(ctx, 'manage_guild'):
        return
    s = '```\n'
    for x in sorted(list(set(cmds).difference(udcmds))):
        s += x + (22-len(x))*' '
    s = s[:-1] + "```"
    await ctx.channel.send(s)
    return

@client.command()
async def undisableablecommands(ctx):
    if await hm.noperms(ctx, 'manage_guild'):
        return
    s = '```\n'
    for x in sorted(udcmds):
        s += x + (22-len(x))*' '
    x = '<Some hidden ones>'
    s += x + (22-len(x))*' '
    s = s[:-1] + "```"
    await ctx.channel.send(s)
    return

@client.command()
async def enable(ctx):
    if await hm.noperms(ctx, 'manage_guild'):
        return
    if await hm.helpredirect(ctx, client): return
    servers = hm.cmds()
    sid = str(ctx.guild.id)
    server = servers.get(sid)
    if not server: return
    cmc = ctx.message.content.split(" ")[1:]
    if len(cmc) > 0:
        for x in cmc:
            if x in cmds:
                server.remove(x)
            elif x == "all":
                for y in list(set(cmds).difference(udcmds)):
                    server.remove(y)
                break
    else: return
    servers.update({sid:server})
    hm.updatecmds(servers)
    await ctx.channel.send("Success")


@client.command()
async def purge(ctx):
    if not ctx.guild:
        async for x in ctx.channel.history(limit=None):
            if x.author.id == client.user.id:
                await x.delete()
        return
    if await hm.noperms(ctx, 'manage_messages'):
        return
    if await hm.helpredirect(ctx, client): return
    cmc = ctx.message.content.split()[1:]
    
    
    '''Evaluate command'''
    deletable = []
    protected = []
    channels = []
    otherints = []
    messagetimes = []
    for x in cmc:
        if target := hm.gettarget(ctx, x):
            deletable.append(target)
            continue
        if not (target := hm.gettarget(ctx, x[1:])):
            target = hm.gettarget(ctx, x[:-1])
        if target:
            protected.append(target)
            continue
        if channel := hm.getchannel(ctx.guild, x):
            channels.append(channel)
            continue
        try:
            message = await ctx.channel.fetch_message(x)
            messagetimes.append(message.created_at)
            continue
        except: pass
        try:
            otherints.append(int(x))
            continue
        except: pass
    if len(otherints) == 0 and not len(messagetimes):
        otherints.append(1)
    for x in otherints:
        if x > 1000:
            return
    if (mtl := len(messagetimes)) == 1:
        messagetimes.append(ctx.message.created_at)
        mtl = 2
    messagetimes = sorted(messagetimes, reverse=True)
    if mtl % 2 == 1:
        messagetimes = messagetimes[mtl//2:] + messagetimes[:mtl//2+1]
    
    '''Evaluate individual messages for deletion'''
    todel = []
    todelold = []
    totdel = 1
    todel.append(ctx.message)
    messages = []
    messages.append(f'{str(ctx.message.author)}: {ctx.message.content}')
    skip = False
    lim = 2*sum(otherints) or None
    dootherints = False if len(otherints) == 0 else True
    async for x in ctx.channel.history(limit=lim if lim == None or lim > 100 else 100):
        if x.content == ctx.message.content:
            continue
        if x.pinned:
            continue
        if protected:
            if x.author in protected or not set(protected).isdisjoint(x.author.roles):
                continue
        if deletable:
            if not x.author in deletable and set(deletable).isdisjoint(x.author.roles):
                continue
        if dootherints:
            if otherints[0] == 0:
                del otherints[0]
                skip = not skip
            if len(otherints) == 0:
                break
        t = (datetime.utcnow() - x.created_at).total_seconds()
        if t < 2 + len(otherints)//2:
            continue
        if skip:
            otherints[0] -= 1
            continue
        if len(messagetimes):
            if messagetimes[1] >= x.created_at:
                if len(messagetimes) > 2:
                    messagetimes = messagetimes[2:]
                    continue
                else:
                    break
            if messagetimes[0] <= x.created_at:
                continue
        if t > 1200000:
            todelold.append(x)
        else:
            todel.append(x)
            totdel += 1
        messages.append(f'{str(x.author)}: {x.content}')
        if dootherints:
            otherints[0] -= 1

    '''Actually delete the messages'''
    while totdel > 100:
        await ctx.channel.delete_messages(todel[:100])
        todel = [x for x in todel if x not in todel[:100]]
        totdel -= 100
    await ctx.channel.delete_messages(todel[:totdel])
    for x in todelold:
        await x.delete()
        
    '''Report deleted messages to deletion-log'''
    mov = f'Message{"s were" if len(messages)>2 else " was"} moved from {ctx.channel.mention} by me, with purge, at {ctx.author.name}\'s command\n'
    for x in reversed(messages[1:]):
        mov += x + '\n'
    mov = mov[:-1][:1996]
    mov += ''
    if len(channels) > 0 and len(messages)>1:
        for x in channels:
            if x.permissions_for(ctx.author).send_messages:
                await x.send(mov)
    
    servers = tilndb.deloggedchannels.find_one()
    gid = str(ctx.message.guild.id)
    channelids = servers.get(gid) or []
    if ctx.message.channel.id in channelids:
        return
    s = f'List of messages deleted in {ctx.channel.mention} by my purge command, newest to oldest:```'
    for x in messages:
        s += x + '\n'
    s = s[:-1][:1996]
    s += '```'
    for x in ctx.guild.text_channels:
        if x.name == 'deletion-log' and len(messages):
            await x.send(s)
    
# @client.command()
# async def purgethewholechannel(ctx):
#     if not ctx.channel.permissions_for(ctx.author).manage_messages:
#         await ctx.channel.send("You don't have permission to use that command.")
#         return
#     async for x in ctx.channel.history(limit=None):
#         await x.delete()

# 

@client.command()
async def collectpoll(ctx):
    if await hm.helpredirect(ctx, client): return
    cmc = ctx.message.content.split(" ")[1:]
    
    channel = None
    trgdic = {}
    num = None
    before = None
    message = None
    for x in range(len(cmc)):
        if cmc[x].lower() == 'before':
            if hm.isdigit(cmc[x+1]):
                n = int(cmc[x+1])
                before = await (channel or ctx.channel).fetch_message(n)
                x += 1
                continue
        if not channel:
            channel = hm.getchannel(ctx.guild, cmc[x])
            if channel:
                continue    
            
        target = hm.gettarget(ctx, cmc[x])
        if target:
            for y in range(x+1, len(cmc)):
                if hm.isdigit(cmc[y]):  
                    trgdic.update({target:float(cmc[y])})
                    break
            if not trgdic.get(target):
                await ctx.channel.send("You have failed to provide a valid role or member multiplier.")
                return
            continue
        
        if not message and hm.isdigit(cmc[x]):
            n = int(cmc[x])
            if n > 9000000000000000:
                message = await (channel or ctx.channel).fetch_message(n)
                if message:
                    continue
            
        if not num and hm.isdigit(cmc[x]):
            n = int(cmc[x])
            if n < 10000000000000000:
                num = n
                continue
    if not channel:
        channel = ctx.channel
    if not message:
        async for x in channel.history(limit=1):
            message = x
    if not num:
        num = 1
    btime = before.created_at if before else datetime.utcnow()
        
#     items = {'polltitle': polltitle, 'emoji': pollemoji, 'options': polloptions, 'responses': {}}
    global rankedpairsf
    if not rankedpairsf:
        rankedpairsf = tilndb.rankedpairs.find_one()
    rankedpairs = copy.deepcopy(rankedpairsf.get(str(message.id)))
    if rankedpairs:
        starpc = hm.rpcollection(rankedpairs, trgdic, ctx, btime)
        supertally = starpc[0]
        optionstable = starpc[1]
        s = '```'
        for x in supertally:
            s2 = ''
            for y in optionstable[x[0]]:
                s2 += f' {y},'
            s2 = s2[:-1]
            s += f'\n{x[1]}. {x[0]}{s2}'
        await ctx.send(s + '```')
        
    else:
        hitmessage = False
        i = 0
        dic = {}
        async for x in channel.history():
            if message == x:
                hitmessage = True
            if not hitmessage: continue
            s = ""
            if x.reactions:
                i += 1
                mes = x.content.split("\n")
                for y in x.reactions:
                    ec = -1
                    async for z in y.users():
                        mult = trgdic.get(z)
                        if not mult and z in ctx.guild.members:
                            for w in z.roles:
                                mult = trgdic.get(w)
                                if mult:
                                    break
                        if not mult:
                            mult = 1
                        if z in ctx.guild.members and z.joined_at < btime:
                            ec += mult
                    if int(ec) == ec:
                        ec = int(ec)
                    for z in mes:
                        if str(y.emoji) in z or (type(y.emoji) != str and y.emoji.name in z):
                            dic.update({z: ec})
                            s += '\n{}: {}'.format(z, str(ec))
                            break
                    if not dic:
                        s += "\n" + str(y.emoji) + ": " + str(ec)
                if not dic:
                    s = x.content + s
                if not dic:
                    await ctx.channel.send(s)
                if i >= num:
                    break
        if dic:
            s = ""
            with open('poll.csv', 'w') as file:
                for k in sorted(dic, key=dic.get, reverse=True):
                    s += k + ": " + str(dic[k]) + "\n"
                    file.write(str(k.replace(",", "").encode("utf-8")) + "," + str(dic[k]) + "\n")
            file = discord.File('poll.csv')
            await ctx.channel.send(s[:-1], file=file)
        
@client.command()
async def singleoption(ctx):
    if not ctx.channel.permissions_for(ctx.author).manage_messages:
        await ctx.channel.send("You don't have permission to use that command.")
        return
    
    cmc = ctx.message.content.split(" ")[1:]
    
    gid = ctx.guild.id
    cid = ctx.channel.id
    if len(cmc) > 0:
        mid = cmc[0]
    else:
        temp = await ctx.channel.history().flatten()
        mid = temp[1].id
    global sopf
    if not sopf:
        sopf = tilndb.singleoptionpolls.find_one()
    guild = sopf.get(str(gid)) or {}
    chan = guild.get(str(cid)) or {}
    mes = not chan.get(str(mid))
    
    chan.update({str(mid):mes})
    guild.update({str(cid):chan})
    sopf.update({str(gid):guild})
    tilndb.singleoptionpolls.replace_one({}, sopf)
        
    global mes_sageid
    mes_sageid = ctx.message.id
    await ctx.message.delete()

@client.command()
async def rankedpairs(ctx):
    if not ctx.channel.permissions_for(ctx.author).manage_messages:
        await ctx.channel.send("You don't have permission to use that command.")
        return
    if await hm.helpredirect(ctx, client): return
    cmc = hm.groupedsplit(ctx.message.content)[1:]
    
    channel = None
    polltitle = ''
    polloptions = []
    for x in cmc:
        if not channel:
            channel = hm.getchannel(ctx.guild, x)
            if channel:
                continue
        if not polltitle:
            polltitle = x
            continue
        polloptions.append(x)
    if not len(polloptions):
        mes = 'No options specified'
        try: await ctx.send(mes)
        except: await ctx.author.send(mes)
        return
    if len(polloptions) > 20 or len(polloptions) < 3:
        mes = 'There is currently a maximum of 20 polloptions and a minimum of 3.'
        try: await ctx.send(mes)
        except: await ctx.author.send(mes)
        return
    if not channel: channel = ctx.channel
    polloptions = sorted(polloptions)
    
    s = f'React with your #1 choice and you will be DM\'d more polls to vote upon. Re-react to this poll to revote.\n{polltitle}'
    poll = hm.makeRPpoll(polloptions)
    s += poll[0]
    messageid = await channel.send(s)
    pollemoji = poll[1]
    for x in pollemoji:
        await messageid.add_reaction(x)
    messageid = messageid.id
    
    items = {'polltitle': polltitle, 'emoji': pollemoji, 'options': polloptions, 'responses': {}}

    global rankedpairsf
    if not rankedpairsf:
        rankedpairsf = tilndb.rankedpairs.find_one()
    rankedpairsf.update({str(messageid): items})
    tilndb.rankedpairs.replace_one({}, rankedpairsf)

# @client.command()
# async def rankedpairsold(ctx):
#     if await hm.helpredirect(ctx, client): return
#     cmc = ctx.message.content.split(" ")[1:]
#     votes = {}
#     alloptions = []
#     after = await ctx.channel.fetch_message(int(cmc[0]))
#     before =  await ctx.channel.fetch_message(int(cmc[1])) if len(cmc) > 1 else None
#     async for x in ctx.channel.history(limit=None, after=after, before=before):
#         if x == ctx.message:
#             continue
#         if x.author.id in votes.keys():
#             continue
#         thesevotes = x.content.split('\n')
#         for y in thesevotes:
#             if y not in alloptions:
#                 alloptions.append(y)
#         votes.update({x.author.id: sorted(set(thesevotes), key=thesevotes.index)})
#     
#     
#     winners = []
#     for x in list(itertools.combinations(alloptions, 2)):
#         tally = [0, 0]
#         for y in votes.values():
#             pos = None
#             if x[0] in y:
#                 pos = y.index(x[0])
#             if x[1] in y:
#                 if pos is not None:
#                     if y.index(x[1]) < pos:
#                         tally[1] += 1
#                     else:
#                         tally[0] += 1
#         if tally[0] > tally[1]:
#             winners += [x[0], x[0]]
#         elif tally[1] > tally[0]:
#             winners += [x[1], x[1]]
#         else:
#             winners += [x[0], x[1]]
#     
#     tally = [[x,winners.count(x)] for x in set(winners)] 
#     tally = sorted(tally, key=lambda x: x[1], reverse=True)
#     s = '```'
#     count = 1
#     for x in tally:
#         flt = int(x[1])/2
#         choppablefloat = int(flt) if int(flt) == flt else flt
#         s += f'\n{count}. {x[0]}: ({choppablefloat})'
#         count += 1
#     await ctx.send(s + '```')

@client.command()
async def checktestresults(ctx):
    if await hm.helpredirect(ctx, client): return
    cmc = ctx.message.content.split(" ")[1:]
    
    chan = None
    num = 0
    for x in cmc:
        if not chan:
            chan = hm.getchannel(ctx.guild, x)
            if chan: continue
        if not num:
            try:
                num = int(x)
                continue
            except: ""
                
    count = 0
    results = {}
    messages = await chan.history(limit=num*2).flatten()
    for x in reversed(messages):
        if count == num:
            break
        rea = x.reactions
        if not rea:
            continue
        for y in rea:
            async for z in y.users():
                urs = results.get(z.name) or []
                urs.append(y.emoji)
                results.update({z.name:urs})
        count += 1
        for k, v in results.items():
            if len(v) < count:
                v.append('0⃣')
                results.update({k:v})
        
    emojdic = {}
    for x, y in zip(emojAN, 'abcdefghijklmnopqrstuvwxyz0123456789'):
        emojdic.update({x:y})
    
    results2 = {}
    for k, v in results.items():
        for x in v:
            if x == '0⃣':
                v.remove('0⃣')
        results2.update({k:v})
        
    s = ''
    for k in sorted(results.keys(), key=lambda x: len(results2[x]), reverse=True):
        s += f'"{k}": '
        for x in ["" + emojdic[a] + "" for a in results[k]]:
            s += x
        s += '\n'
    
            
    splitres = s.split('\n')
#     print(len(splitres), len(results), results)
    tempres = ""
    for x in range(len(splitres)):
        tempres += splitres[x] + '\n'
        if x+1 == len(splitres) or len(tempres + splitres[x+1]) > 2000:
#             await ctx.send(tempres[:-1])
            tempres = ""
    await ctx.message.delete()
            
    for k, v in results.items():
        for x in range(len(v)):
            v[x] = emojdic[v[x]]
        results.update({k:v})
    for k, v in results.items():
        if len(v)<17:
            while len(v)<17:
                v.insert(0, '0')
            results.update({k: v})
    res = {}
    for k, v in results.items():
        #['adaabeib', 'bdaabeib', 'adaaceib', 'bdaaceib']
        for z in ['epgdyyabcebbcdacw', 'epfdyyabcebbcdacw', 'epgdyydbcebbcdacw', 'epfdyydbcebbcdacw']:
            count = 0
            for x, y in zip(z, v):
                if x == y :
                    count += 1
                    if x == 'g': count += 1
            if count >= (res.get(k) or 0):
                res.update({k:count})
    res2 = {}
    for k, v in results.items():
        #['dabeaabi', 'dadeaabi']
        for z in ['asaennccddwwwwwaw', 'aseennccddwwwwwaw']:
            count = 0
            for x, y in zip(z, v):
                if x == y:
                    count += 1
            if count >= (res2.get(k) or 0):
                res2.update({k:count})
#     for k, v, u in zip(res.keys(), res.values(), res2.values()):
#         res.update({k:(v-u)})
#     for (k, v), (j, u) in zip(sorted(res.items(), key=lambda x: x[0]), sorted(res2.items(), key=lambda x: x[0])):
    RW = ''
    for k, v, u in sorted(zip(res.keys(), res.values(), res2.values()), key=lambda x: (x[1]-x[2], x[2]*-1, x[1])):
        s = ''
        for x in results.get(k):
            RW += f'{v},{u} {k}{" "*(25-len(k))}{s}\n'
#        if v > 5:
#            print(results.get(k))
    print(RW)

 
@client.command()
async def reminder(ctx):
    if await hm.helpredirect(ctx, client): return
    cmc = ctx.message.content.split(" ", 2)[1:]
    res = hm.dehumantime(cmc[0])
    num = res[0]
    tim = res[1]
    if len(tim) > 0:
        num += float(tim)
    
    auth = ctx.author.mention
    global mes_sageid
    mes_sageid = ctx.message.id
    await ctx.message.delete()
    await asyncio.sleep(num)
    rem = ""
    if len(cmc) > 1:
        rem = cmc[1]
    secs = math.trunc(num)
    fortim = ""
    if secs > 24*3600:
        n = math.trunc(secs/(24*3600))
        secs -= n*24*3600
        fortim += str(n) + 'd'
    if secs > 3600:
        n = math.trunc(secs/3600)
        secs -= n*3600
        fortim += str(n) + 'h'
    if secs > 60:
        n = math.trunc(secs/60)
        secs -= n*60
        fortim += str(n) + 'm'
    if secs > 0:
        fortim += str(secs) + 's'
    
    await ctx.channel.send(auth + ", your reminder is ready with reason: " + '"' + rem.replace("\\", "") + '"' + "```The command invocation message for this message was sent " + fortim + " ago.```")


# @client.command()
# async def exclusivizeroles(ctx):
#     if not ctx.channel.permissions_for(ctx.author).manage_roles:
#         await ctx.channel.send("You don't have permission to use that command.")
#         return
#     cmc = ctx.message.content.split(" ")[1:]
#     exroles = []
#     strexroles = []
#     for x in cmc:
#         r = discord.utils.get(ctx.guild.roles, name=x.replace("_", " "))
#         if not r:
#             await ctx.channel.send(x + " is not recognized as a valid role.")
#             return
#         else: exroles.append(r)
#         strexroles.append(x.replace("_", " "))
# 
#     file = open('jsons/exclusiveroles.json', 'r+')
#     guilds = json.load(file)
#     sid = str(ctx.guild.id)
#     guild = guilds.get(sid) or []
#     s = ""
#     add = True
#     for x in guild:
#         if strexroles == x.split(":"):
#             add = False
#             guild = guild.replace("," + x, "")
#     if add:
#         for x in strexroles:
#             s += x + ":"
#         s = s[:-1]
#     guild.append(s)
#     guilds.update({sid:guild})
#     file = open('jsons/exclusiveroles.json', 'w+')
#     file.write(json.dumps(guilds))

        
@client.command()
async def timedroles(ctx):
    if not ctx.channel.permissions_for(ctx.author).manage_roles:
        await ctx.channel.send("You don't have permission to use that command.")
        return
    if await hm.helpredirect(ctx, client): return
    cmc = ctx.message.content.split(" ")
    ml = ctx.guild.members
    rta = []
    rtr = []
    num = float(cmc[1][:-1])
    if cmc[1].endswith("y"):
        num *= 365*24*3600
    elif cmc[1].endswith("o"):
        num *= 30.5*24*3600
    elif cmc[1].endswith("w"):
        num *= 7*24*3600
    elif cmc[1].endswith("d"):
        num *= 24*3600
    elif cmc[1].endswith("h"):
        num *= 3600
    elif cmc[1].endswith("m"):
        num *= 60
    elif cmc[1].endswith("s"):
        num = num
    else:
        num = float(cmc[1])
    for m in ml:
        t = (ctx.message.created_at - m.joined_at).total_seconds()
        if t > num and not m.bot:
            for x in cmc[2:]:
                if x.startswith("!"):
                    r = discord.utils.get(roles, name=x[1:].replace("_", " "))
                    if r:
                        rtr.append(r)
                else:
                    r = discord.utils.get(roles, name=x.replace("_", " "))
                    if r:
                        rta.append(r)
            await hm.updateroles(ctx, rta, rtr, client, roles, specuser=m)


# @client.command()
# async def linkroles(ctx):
#     if not ctx.channel.permissions_for(ctx.author).manage_roles:
#         await ctx.channel.send("You don't have permission to use that command.")
#         return
#     cmc = ctx.message.content.split(" ")[1:]
#     rec = discord.utils.get(ctx.guild.roles, name=cmc[0].replace("_", " "))
#     torec = discord.utils.get(ctx.guild.roles, name=cmc[1].replace("_", " "))
#     file = open('jsons/linkedroles.json', 'r+')
#     guilds = json.load(file)
#     sid = str(ctx.guild.id)
#     guild = guilds.get(sid) or []
#     add = True
#     for x in guild:
#         if rec.name == x.split(":")[0] and torec.name == x.split(":")[1]:
#             add = False
#             guild.remove(x)
#     if add:
#         guild.append(rec.name + ":" + torec.name)
#     guilds.update({sid:guild})
#     file = open('jsons/linkedroles.json', 'w+')
#     file.write(json.dumps(guilds))


@client.command()
async def privatechannels(ctx):
    if not ctx.channel.permissions_for(ctx.author).manage_guild or not ctx.channel.permissions_for(ctx.author).manage_channels:
        await ctx.channel.send("You don't have permission to use that command.")
        return
    if not ctx.channel.permissions_for(discord.utils.get(ctx.guild.members, id=447268676702437376)).manage_channels:
        await ctx.channel.send("I require the manage channels permission for this.")
        return
    if await hm.helpredirect(ctx, client): return
    cmc = hm.groupedsplit(ctx.message.content)[1:]
    PCs = tilndb.privatechannels.find_one()
    gid = str(ctx.guild.id)
    guildPC = PCs.get(gid) or {}
        
    if len(cmc) == 1:
        if hm.isdigit(cmc[0]):
            cat = discord.utils.get(ctx.guild.categories, id=int(cmc[0]))
            role = discord.utils.get(ctx.guild.roles, id=int(cmc[0]))
        else:
            cat = discord.utils.get(ctx.guild.categories, name=cmc[0].replace('[space]', ' '))
            role = discord.utils.get(ctx.guild.roles, name=cmc[0].replace('[space]', ' ')) or discord.utils.get(ctx.guild.roles, mention=cmc[0])
        if cat:
            cid = str(cat.id)
            if guildPC.get(cid):
                guildPC.update({cid: False})
                await ctx.channel.send("Succesfully disallowed free creation in " + cat.name + " even if freecreation is enabled.")
            elif not guildPC.get(cid):
                guildPC.update({cid: True})
                await ctx.channel.send("Succesfully allowed free creation in " + cat.name + " while freecreation is enabled.")
        elif role:
            rid = str(role.id)
            if guildPC.get(rid):
                guildPC.update({rid: False})
                await ctx.channel.send("Succesfully disallowed free creation by " + role.name + " even if freecreation is enabled.")
            elif guildPC.get(rid) == False:
                guildPC.pop(rid)
                await ctx.channel.send("Succesfully disallowed free creation by " + role.name + ", but only while freecreation is disabled")
            else:
                guildPC.update({rid: True})
                await ctx.channel.send("Succesfully allowed free creation by " + role.name + " even if freecreation is disabled")
        else:
            if cmc[0].lower() == 'enable':
                guildPC.update({'freecreation': True})
                await ctx.channel.send("Succesfully enabled free creation of private channels")
            elif cmc[0].lower() == 'disable':
                guildPC.update({'freecreation': False})
                await ctx.channel.send("Succesfully disabled free creation of private channels")
            elif hm.isdigit(cmc[0]):
                if int(cmc[0]) >= 0 and int(cmc[0]) <= 100:
                    prev = guildPC.get('max')
                    guildPC.update({'max': int(cmc[0])})
                    await ctx.channel.send(f"Set the maximum private channels creatable by any individual that can create from {prev} to {int(cmc[0])}")
                else:
                    await ctx.channel.send("Invalid maximum free creations")
            else: 
                ctx.message.content = "!?help privatechannels"
                await client.process_commands(ctx.message)
                return
    elif len(cmc) == 2 or len(cmc) == 3 or len(cmc) == 4:
        if '#' in cmc[0]:
            owner = discord.utils.get(ctx.guild.members, name=cmc[0].split('#')[0], discriminator=cmc[0].split('#')[1])
        else:
            owner = discord.utils.get(ctx.guild.members, mention=cmc[0]) or discord.utils.get(ctx.guild.members, id=int(cmc[0]))
        oid = str(owner.id)
        if len(cmc[1]) > 100:
                await ctx.channel.send("Channel name too long")
                return
        if hm.isdigit(cmc[1]):
            chan = discord.utils.get(ctx.guild.channels, id=int(cmc[1]))
            if not chan:
                await ctx.channel.send("Invalid channelid")
                return   
        elif len(cmc) == 2:
            chan = await hm.createpc(ctx, owner)
        elif len(cmc) == 3:
            cmc[2] = cmc[2].replace('[space]', ' ')
            chan = await hm.createpc(ctx, owner, cmc[2])
        elif len(cmc) == 4:
            cmc[2] = cmc[2].replace('[space]', ' ')
            chan = await hm.createpc(ctx, owner, cmc[2], True)
        chid = str(chan.id)
        chanlist = guildPC.get(oid) or []
        if chid not in chanlist:
            chanlist.append(chid)
            guildPC.update({oid: chanlist})
            target = hm.gettarget(ctx, oid)
            ow = {'read_messages':True, 'manage_messages':True, 'priority_speaker':True, 'move_members':True}
            overwrite = chan.overwrites_for(target)
            overwrite.update(**ow)
            await chan.set_permissions(target, overwrite=overwrite)
            await ctx.channel.send("Added owner")
        elif chid in chanlist:
            chanlist.remove(chid)
            guildPC.update({oid: chanlist})
            target = hm.gettarget(ctx, oid)
            ow = {'read_messages':True, 'manage_messages':None, 'priority_speaker':None, 'move_members':None}
            overwrite = chan.overwrites_for(target)
            overwrite.update(**ow)
            await chan.set_permissions(target, overwrite=overwrite)
            await ctx.channel.send("Removed owner")
    
    PCs.update({gid:guildPC})
    
    tilndb.privatechannels.replace_one({}, PCs)


@client.command()
async def pchan(ctx):
    if not ctx.channel.permissions_for(discord.utils.get(ctx.guild.members, id=447268676702437376)).manage_channels:
        await ctx.channel.send("I require the manage channels permission for this.")
        return
    if await hm.helpredirect(ctx, client): return
    cmc = hm.groupedsplit(ctx.message.content)[1:]
    PCs = tilndb.privatechannels.find_one()
    gid = str(ctx.guild.id)
    guildPC = PCs.get(gid)
    if not guildPC:
        await ctx.channel.send("Requires !?privatechannels to be used first.")
        return
    
    z = cmc[0].lower()
    if z == "create" or z == "delete":
        ctx.message.content = "!?help pchan{}".format(z)
        await client.process_commands(ctx.message)
        return
    
    cmc[1] = cmc[1].replace("[space]", ' ')
    target = hm.gettarget(ctx, cmc[1])
    if not target:
        await ctx.channel.send("Invalid target")
        return
        
    chan = None
    if len(cmc) == 3:
        if hm.isdigit(cmc[2]):
            chan = discord.utils.get(ctx.guild.channels, id=int(cmc[2]))
        elif not chan:
            chan = discord.utils.get(ctx.guild.channels, mention=cmc[2]) or discord.utils.get(ctx.guild.channels, name=cmc[2].replace('[space]', ' '))
    if not chan:
        chan = ctx.channel
    chid = str(chan.id)
    
    chans = guildPC.get(str(target.id)) or []
    if type(chans) == list:
        if chid in chans:
            await ctx.channel.send("You can't target another owner!")
            return
    
    chans = guildPC.get(str(ctx.author.id)) or []
    if not chid in chans:
        await ctx.channel.send("You are not the owner of this channel")
        return
    
    s = "Success"
    perms = chan.overwrites_for(target)
    if cmc[0].lower() == "invite":
        overwrite = discord.PermissionOverwrite(read_messages=True)
        s = f'Invited {target}'
    elif cmc[0].lower() == "kick":
        overwrite = discord.PermissionOverwrite(read_messages=None)
        s = f'Kicked {target}'
    elif cmc[0].lower() == "superkick":
        overwrite = discord.PermissionOverwrite(read_messages=False)
        s = f'Superkicked {target}'
    elif cmc[0].lower() == "setspectator":
        overwrite = discord.PermissionOverwrite(read_messages=True, send_messages=False, connect=False)
    elif cmc[0].lower() == "setlistener":
        overwrite = discord.PermissionOverwrite(read_messages=True, send_messages=False, connect=True, speak=False)
    elif cmc[0].lower() == "transferownership":
        if not discord.utils.get(ctx.guild.members, id=target.id):
            await ctx.channel.send("You can't give ownership away to a role!")
            return
        overwrite = discord.PermissionOverwrite(read_messages=True, manage_messages=True, priority_speaker=True, move_members=True)
        ow = discord.PermissionOverwrite(read_messages=True, manage_messages=None, priority_speaker=None, move_members=None)
        await chan.set_permissions(ctx.author, overwrite=ow)
        
        achans = guildPC.get(str(ctx.author.id))
        tchans = guildPC.get(str(target.id)) or []
        achans.remove(str(chan.id))
        tchans.append(str(chan.id))
        guildPC.update({str(ctx.author.id):achans})
        guildPC.update({str(target.id):tchans})
        
        PCs.update({gid:guildPC})
        tilndb.privatechannels.replace_one({}, PCs)
        
        s = "Transferred ownership to " + target.name
    elif cmc[0].lower() == "manage_messages":
        if type(chan) == discord.channel.TextChannel:
            overwrite = discord.PermissionOverwrite(read_messages=perms.read_messages, send_messages=perms.send_messages, manage_messages=None if perms.manage_messages else True)
            if chan.permissions_for(target).manage_messages:
                s = "Manage Messages revoked from " + str(target)
            elif not perms.manage_messages:
                s = "Manage Messages given to " + str(target)
        else:
            await ctx.channel.send("Cannot be given in a VoiceChannel")
    elif cmc[0].lower() == "priority_speaker":
        if type(chan) == discord.channel.VoiceChannel:
            overwrite = discord.PermissionOverwrite(read_messages=perms.read_messages, priority_speaker=None if perms.priority_speaker else True, move_members=perms.move_members, connect=perms.connect, speak=perms.speak)
            if perms.priority_speaker:
                s = "Priority Speaker revoked from " + str(target)
            elif not perms.priority_speaker:
                s = "Priority Speaker given to " + str(target)
        else:
            await ctx.channel.send("Cannot be given in a TextChannel")    
    elif cmc[0].lower() == "move_members":
        if type(chan) == discord.channel.VoiceChannel:
            overwrite = discord.PermissionOverwrite(read_messages=perms.read_messages, move_members=None if perms.move_members else True, priority_speaker=perms.priority_speaker, connect=perms.connect, speak=perms.speak)
            if perms.priority_speaker:
                s = "Priority Speaker revoked from " + str(target)
            elif not perms.priority_speaker:
                s = "Priority Speaker given to " + str(target)
        else:
            await ctx.channel.send("Cannot be given in a TextChannel")
    else:
        ctx.message.content = "!?help pchan"
        await client.process_commands(ctx.message)
        return
    await chan.set_permissions(target, overwrite=overwrite)
    await ctx.channel.send(s)


@client.command()
async def pchancreate(ctx):
    if not ctx.channel.permissions_for(discord.utils.get(ctx.guild.members, id=447268676702437376)).manage_channels:
        await ctx.channel.send("I require the manage channels permission for this.")
        return
    if await hm.helpredirect(ctx, client): return
    cmc = ctx.message.content.split(" ")[1:]
    PCs = tilndb.privatechannels.find_one()
    gid = str(ctx.guild.id)
    guildPC = PCs.get(gid)
    
    testfc = True
    deny = False
    for x in reversed(ctx.author.roles):
        rid = str(x.id)
        if guildPC.get(rid):
            testfc = False
            deny = False
            break
        elif guildPC.get(rid) == False:
            deny = True
            break
        
    if deny == True:
        await ctx.channel.send("You have a role that is disallowed from creating channels. Free creation may also be disabled.")
        return
    if not guildPC.get("freecreation") and testfc:
        await ctx.channel.send("Free creation in this server is disabled")
        return
    
    chan = None
    if hm.isdigit(cmc[0]):
        chan = discord.utils.get(ctx.guild.channels, id=int(cmc[0]))
    elif not chan:
        chan = discord.utils.get(ctx.guild.channels, mention=cmc[0]) or discord.utils.get(ctx.guild.channels, name=cmc[0])
    if chan:
        await ctx.channel.send("Channel already exists")
        return
    owned = guildPC.get(str(ctx.author.id))
    maxi = guildPC.get('max') or 1
    if owned:
        if len(owned) >= maxi:
            await ctx.channel.send("You can't create anymore channels")
            return
    if len(cmc) > 1:
        cmc[1] = cmc[1].replace('[space]', ' ')
        cat = discord.utils.get(ctx.guild.categories, name=cmc[1])
        if not cat and hm.isdigit(cmc[1]):
            cat = discord.utils.get(ctx.guild.categories, id=int(cmc[1]))
        if not cat:
            await ctx.channel.send("Category doesn't exist")
            return
        elif not guildPC.get(str(cat.id)) and not cat.name == "private channels":
            await ctx.channel.send("Free creation in this category is disabled")
            return
        else:
            if len(cmc) > 2:
                cmc[2] = cmc[2].replace('[space]', ' ')
                chan = await hm.createpc(ctx, ctx.author, str(cat.id), chin=0, voice=True)
            else:
                chan = await hm.createpc(ctx, ctx.author, str(cat.id), chin=0)
    
    else:
        chan = await hm.createpc(ctx, ctx.author, chin=0)
    
    
        
    chid = str(chan.id)
    aid = str(ctx.author.id)
    chans = guildPC.get(aid) or []
    chans.append(chid)
    guildPC.update({aid:chans})
    
    PCs.update({gid:guildPC})
    tilndb.privatechannels.replace_one({}, PCs)
    
@client.command()
async def pchandelete(ctx):
    if not ctx.channel.permissions_for(discord.utils.get(ctx.guild.members, id=447268676702437376)).manage_channels:
        await ctx.channel.send("I require the manage channels permission for this.")
        return
    if await hm.helpredirect(ctx, client): return
    cmc = ctx.message.content.split(" ")[1:]
    PCs = tilndb.privatechannels.find_one()
    gid = str(ctx.guild.id)
    guildPC = PCs.get(gid)
    #get channel
    chan = None
    if hm.isdigit(cmc[0]):
        chan = discord.utils.get(ctx.guild.channels, id=int(cmc[0]))
    elif not chan:
        chan = discord.utils.get(ctx.guild.channels, mention=cmc[0]) or discord.utils.get(ctx.guild.channels, name=cmc[0])
    if not chan:
        await ctx.channel.send("Channel doesn't exist")
        return
    chid = str(chan.id)
    if not chid in guildPC.get(str(ctx.author.id)):
        await ctx.channel.send("You are not an owner of this channel")
        return
    #see how many 'own' that channel
    owns = 0
    for k, v in guildPC.items():
        if not hm.isdigit(k) or not type(v) == list:
            continue
        for x in v:
            if x == chid:
                owns += 1
                break
    if owns > 2:
        await ctx.channel.send("Too many owners to delete. Ask an admin if they'll delete it for you.")
        return
    #delete the channel
    await chan.delete(reason="Owner said so")
    await ctx.channel.send("Channel deleted")
    chans = guildPC.get(str(ctx.author.id))
    chans.remove(chid)
    guildPC.update({str(ctx.author.id):chans})
    
    PCs.update({gid:guildPC})
    tilndb.privatechannels.replace_one({}, PCs)
    
@client.command()
async def pchanowned(ctx):
    PCs = tilndb.privatechannels.find_one()
    gid = str(ctx.guild.id)
    guildPC = PCs.get(gid)
    chans = guildPC.get(str(ctx.author.id))
    
    if not chans:
        await ctx.channel.send("You don't own any channels in this server/guild.")
        return
    s = "Channels you own in this server/guild: "
    for x in chans:
        chan = discord.utils.get(ctx.guild.channels, id=int(x))
        if chan:
            s += '\n' + chan.mention + ' '
    await ctx.channel.send(s)

@client.command()
async def pchanrename(ctx):
    PCs = tilndb.privatechannels.find_one()
    gid = str(ctx.guild.id)
    guildPC = PCs.get(gid)
    chans = guildPC.get(str(ctx.author.id))
    if await hm.helpredirect(ctx, client): return
    cmc = ctx.message.content.split(" ")[1:]
    #parse args
    channel = None
    name = None
    for x in cmc:
        if not channel:
            channel = hm.getchannel(ctx.guild, x)
            if channel: continue
        if not name:
            name = x
    channel = channel if channel else ctx.channel 
    if str(channel.id) in chans:
        await channel.edit(name=name)
        await ctx.send("Success")
    else:
        await ctx.send("You do not own this channel")
        
@client.command()
async def pchansettopic(ctx):
    PCs = tilndb.privatechannels.find_one()
    gid = str(ctx.guild.id)
    guildPC = PCs.get(gid)
    chans = guildPC.get(str(ctx.author.id))
    if await hm.helpredirect(ctx, client): return
    cmc = ctx.message.content.split(" ")[1:]
    #parse args
    channel = None
    channame = None
    for x in cmc:
        if not channel:
            channel = hm.getchannel(ctx.guild, x)
            if channel:
                channame = x
                break
    channel = channel if channel else ctx.channel
    channame = channame if channame else ""
    if str(channel.id) in chans:
        await channel.edit(topic=' '.join(cmc).replace(channame, '', 1).replace('  ', ' '))
        await ctx.send("Success")
    else:
        await ctx.send("You do not own this channel")
        
        
@client.command()
async def pchankickyourself(ctx):
    guildPC = hm.openguildjson('jsons/privatechannels.json', str(ctx.guild.id))
#     skc = hm.openguildjson('jsons/selfkickablechannels.json', str(ctx.guild.id))
    cmc = ctx.message.content.split(" ")[1:]
    channel = None
    for x in cmc:
        if not channel:
            channel = hm.getchannel(ctx.guild, x)
        else: break
    channel = channel if channel else ctx.channel
    good = False
    for k, v in guildPC.items():
        superbreak = False
        try:
            for x in v:
                if str(ctx.author.id) == k and x == str(channel.id):
                    await ctx.send("You cannot kick yourself from a channel you own!")
                    return
                if x == str(channel.id):
                    good = True
                    superbreak = True
                    break
        except: ""
        if superbreak: break
    if not good: return
    overwrite = discord.PermissionOverwrite(read_messages=False)
    await channel.set_permissions(ctx.author, overwrite=overwrite)
    if channel == ctx.channel:
        global mes_sageid
        mes_sageid = ctx.message.id
        await ctx.message.delete()
    else:
        await ctx.send(f"Successfully kicked yourself from {channel.mention}.")
    
@client.command()
async def getchannelmembers(ctx):
    members = ctx.channel.members
    if len(members) > 250:
        await ctx.send('A large-scale list of members has not been coded yet.')
        return
    members2 = []
    for x in sorted(members, key=lambda x: x.name.lower()):
        if x.bot:
            continue
        if ctx.channel.permissions_for(x).manage_channels or (ctx.channel.permissions_for(x).manage_messages and ctx.channel.permissions_for(x).ban_members):
            if (PO := ctx.channel.overwrites.get(x)) and PO.pair()[0].value & discord.Permissions.read_messages.flag != 0:
                members2.append(x) 
        else:
            members2.append(x)
    s = f'Member list(-Bots,Auto-invitees not specifically invited)({len(members2)} members):```\n'
    for x in members2:
        s += f'{str(x)}\n'
    await ctx.send(f'{s}```')
        
@client.command()
async def setprefix(ctx):
    if await hm.noperms(ctx, 'manage_guild'):
        return
    if await hm.helpredirect(ctx, client): return
    np = ctx.message.content.split(' ', 1)[1]
    hm.setprefix(str(ctx.guild.id), np)
    await ctx.channel.send(f"prefix changed to `{np}`")
    
    
async def prune2(ctx, prunemems=False):
    if await hm.noperms(ctx, 'manage_guild', 'kick_members'):
        return
    if await hm.helpredirect(ctx, client): return
    cmc = ctx.message.content.split(" ")[1:]
    days = None
    prottargs = []
    protsome = False
    for x in cmc:
        if not days:
            if x.isdigit():
                days = int(x)
                continue
        if x == 'all':
            roles = ctx.guild.roles
            roles.remove(ctx.guild.default_role)
            prottargs.extend(roles)
            protsome = True
            continue
        target = hm.gettarget(ctx, x)
        if target:
            prottargs.append(target)
            protsome = True
            continue
        target = hm.gettarget(ctx, x.replace('-', '', 1))
        if target:
            prottargs.remove(target)
            continue
    if not protsome:
        await ctx.send('As a precautionary measure against accidents you must protect something from pruning.')
        return
        
    takeawhile = await ctx.send("This may take awhile, Scanning channels...")
    
    allauthors = {"Thisisaplaceholderitem"}
    for channel in ctx.guild.text_channels:
        everyoneisprotected = True
        for x in channel.members:
            protected = False
            if x in prottargs:
                protected = True
                continue
            for y in x.roles:
                if y in prottargs:
                    protected = True
                    break
            if not protected:
                everyoneisprotected = False
                break
        if everyoneisprotected:
            continue
        
        try:
            messages = await channel.history(limit=None, after=ctx.message.created_at - timedelta(days=days)).flatten()
        except: continue
        for x in messages:
            allauthors.add(x.author.id)
        
    if prunemems:
        await takeawhile.edit(content="...kicking members...")
    else:
        await takeawhile.edit(content="...Approximating prunes...")
        
    peoplekicked = []
    for x in ctx.guild.members:
        if x.id in allauthors:
            continue
        if x in prottargs:
            continue
        
        cont = False
        for y in x.roles:
            if y in prottargs:
                cont = True
                break
        if cont:
            continue
        
        memdays = (ctx.message.created_at - x.joined_at).total_seconds()/3600/24
        if memdays < days:
            continue
        
        peoplekicked.append(str(x))
        if prunemems:
            await x.kick(reason='Pruning members')
#         with open('peoplekicked.txt', 'w+') as file:
#         file.write(str(.encode("utf-8")))
    pk = len(peoplekicked)
    if prunemems:
        file = open('peoplekicked.txt', 'w+')
    else:
        file = open('theoreticallypruned.txt', 'w+')
    file.write(str(f"{pk}, {peoplekicked}".encode('utf_8')))
    file.close()
    await takeawhile.delete()
    global mes_sageid
    mes_sageid = ctx.message.id
    if prunemems:
        await ctx.send(content=f'...Done! Total people kicked: {pk}. List of members kicked:', file=discord.File('peoplekicked.txt'))
    else:
        await ctx.send(content=f'...Done! Total people theoretically pruned: {pk}. List of members theoretically pruned:', file=discord.File('theoreticallypruned.txt'))
#         print(f"{len(peoplekicked)}, {peoplekicked}")
    
@client.command()
async def prune(ctx):
    await prune2(ctx, prunemems=True)
@client.command()
async def theoreticalprune(ctx):
    await prune2(ctx)
    

@client.command()
async def report(ctx):
    '''Evaluate command'''
    if await hm.helpredirect(ctx, client): return
    cmc = ctx.message.content.split(' ', 2)[1:]
    member = hm.getmember(ctx.guild, cmc[0])
    if not member:
        await ctx.send("Invalid member")
        return
    try:
        global mes_sageid
        mes_sageid = ctx.message.id
        await ctx.message.delete()
    except: ""
    try:
        reason = cmc[1]
    except:
        await ctx.send("No reason specified")
        return
    
    if reason != 'test':
        '''Store report in reports json'''
        mid = str(member.id)
        reports = tilndb.reports.find_one()
        reasons = reports.get(mid)
        if not reasons:
            reasons = []
        reasons.append(f'{str(ctx.author)}: {reason}')
        reports.update({str(member.id): reasons})
        tilndb.reports.replace_one({}, reports)
    
    '''Post report to reports channel'''
    servers = tilndb.reportchannels.find_one()
    gid = str(ctx.guild.id)
    reportchannels = servers.get(gid) or []
    for x in ctx.guild.text_channels:
        if str(x.id) in reportchannels:
            await x.send(f'Report for: {str(member)}({member.mention})\nBy: {str(ctx.author)}({ctx.author.mention}) in channel: {ctx.channel.mention}\nReason: {reason}')
    

@client.command()
async def reportsfor(ctx):
    if await hm.noperm(ctx, 'manage_guild', 'manage_channels'):
        return
    if await hm.helpredirect(ctx, client): return
    member = hm.getmember(ctx.guild, ctx.message.content.split(' ', 1)[1])
    reports = tilndb.reports.find_one()
    reasons = reports.get(str(member.id))
    s = f'Reports for {str(member)}({member.mention}):```'
    for x in reversed(reasons):
        s += x + '\n'
    s = s[:-1]
    s = s[:1996]
    await ctx.send(s + '```')


@client.command()
async def setreportchannel(ctx):
    if await hm.noperm(ctx, 'manage_guild', 'manage_channels'):
        return
    if await hm.helpredirect(ctx, client): return
    channel = hm.getchannel(ctx.guild, ctx.message.content.split(' ', 1)[1])
    if channel:
        servers = tilndb.reportchannels.find_one()
        gid = str(ctx.guild.id)
        reportchannels = servers.get(gid) or []
        
        chid = str(channel.id)
        if chid in reportchannels:
            reportchannels.remove(chid)
            await ctx.send(f'Removed channel {channel.mention} from report channels')
        else: 
            reportchannels.append(chid)
            await ctx.send(f'Added channel {channel.mention} to report channels')
            
        servers.update({gid: reportchannels})
        tilndb.reportchannels.replace_one({}, servers)
    else:
        await ctx.send("No channel specified")

@client.command()
async def disablelogginghere(ctx):
    if await hm.noperms(ctx, 'manage_channels'):
        return
    
    servers = tilndb.deloggedchannels.find_one()
    gid = str(ctx.guild.id)
    channels = servers.get(gid) or []
    chid = ctx.channel.id
    if chid in channels:
        channels.remove(chid)
        await ctx.send(f'Readded this channel to being logged')
    else: 
        channels.append(chid)
        await ctx.send(f'Removed this channel from being logged')
        
    servers.update({gid: channels})
    tilndb.deloggedchannels.replace_one({}, servers)

# @client.command()
# async def rolepersist(ctx):
#     perms = ctx.channel.permissions_for(ctx.author)
#     if not perms.manage_roles:
#         await ctx.channel.send("You don't have permission to use that command.")
#         return
#     cmc = ctx.message.content.split(' ')[1:]
#     if not cmc:
#         ctx.message.content = '!?help rolepersist'
#         await client.process_commands(ctx.message)
#      
#     '''Command arguments to useful things'''
#     role = None
#     member = None
#     for x in cmc:
#         if not role:
#             role = hm.getrole(ctx.guild, x)
#         if not member:
#             member = hm.getmember(ctx.guild, x)
#     if not role:
#         await ctx.send("No role specified")
#         return
#     if not member:
#         await ctx.send("No member specified")
#         return
#      
#     '''Read from the file'''
#     file = open('jsons/rolepersistance.json', 'r+')
#     servers = json.load(file)
#     gid = str(ctx.guild.id)
#     persistedusers = servers.get(gid) or {}
#     mid = str(member.id)
#     persistedroles = persistedusers.get(mid) or []
#      
#     '''Make the changes to the dictionary'''
#     rid = str(role.id)
#     if rid in persistedroles:
#         persistedroles.remove(rid)
#         await ctx.send(f'Removed role {role} from being persisted on member {member}({member.mention})')
#     else:
#         persistedroles.append(rid)
#         await ctx.send(f'Added role {role} to persist on member {member}({member.mention})')
#      
#     '''Write to the file'''
#     persistedusers.update({mid: persistedroles})
#     servers.update({gid: persistedusers})
#     file = open('jsons/rolepersistance.json', 'w+')
#     file.write(json.dumps(servers))


@client.command()
async def define(ctx):
    if await hm.helpredirect(ctx, client): return
    cmc = ctx.message.content.split(" ", 1)[1].lower()
    file = open('dictionary.json', 'r+')
    dictionary = json.load(file)
    file.close()
    s = '```'
    if cmc in dictionary.keys():
        definitions = dictionary[cmc].split('\n\n')
        for x in definitions:
            x = x.replace(' esp.', ' especially')
            if x.startswith("1."):
                counter = 1
                start = 0
                end = 0
                inparen = False
                for y in range(len(x)):
                    if x[y] == '(':
                        inparen = True
                    if x[y] == ')':
                        inparen = False
                    if x[y] == '.':
                        if x[y-1] == str(counter)[-1]:
                            start = y
                            counter += 1
                        elif not inparen:
                            end = y
                        if end > start:
                            s += x[start-1:end+1] + '\n'
                            start = 1000000000
            else:
#                 splitdef = hm.bracesplit(x, ['(', ')'])
                inparen = False
                defi = ''
                for y in x:
                    if y == '(':
                        inparen = True
                    if y == ')':
                        inparen = False
                    if y == '.' and not inparen:
                        break
                    defi += y
                s += f'{defi}.\n'
    if len(s) > 3:
        await ctx.send(f'{s[:1996]}```') 


@client.command()
async def roll(ctx):
    cmcs = ctx.message.content.split(" ")[1:]
    sysrand = random.SystemRandom()
    if len(cmcs) == 0:
        await ctx.channel.send("You rolled a " + str(sysrand.randint(1, 6)) + ".")
    else:
        nsp = NumericStringParser()
        nums = cmcs[0].split("d")
        cha = 0
        if ("+" in nums[1] or "-" in nums[1]) and await nsp.eval(nums[1]):
            if "+" in nums[1]:
                sp = nums[1].split("+")
                cha = Decimal(sp[1])
            else:
                sp = nums[1].split("-")
                cha = Decimal(sp[1]) * -1
            nums[1] = sp[0]
        s = ""
        total = 0
        try:
            n = await nsp.eval(nums[1])
        except:
            return
        dice = int(nums[0] or 1)
        cl = 1994
        mes = 1
        if dice > 2500//len(str(n)):
            await ctx.channel.send("Too many dice of that size")
            return
        for _11 in range(dice):
            rand = sysrand.randint(1, n) + cha
            total += rand
            s += str(rand) + " "
        if dice > 1:
            if len(cmcs)>1:
                try:
                    file = await nsp.eval(str(total) + ''.join(cmcs[1:]))
                    s += str(math.trunc(file))
                except: 
                    print('eyo')
                    print(file, s)
                    return
            else:
                s += str(total)
        if dice < 2:
            try:
                file = await nsp.eval(str(total) + ''.join(cmcs[1:]))
            except: return
            calcres = str(math.trunc(file))
            if ctx.author.id == 115707766714138627 and calcres == "1" and n == 20:
                calcres = str(sysrand.randint(10, 15))
            await ctx.channel.send("You rolled a " + str(calcres) + ".")
        elif len(s) <= mes * cl:
            while(len(s) > cl):
                await ctx.channel.send("```" + s[:cl] + "```")
                s = s[cl:]
            await ctx.channel.send("```" + s + "```")
        else:
            await ctx.channel.send("```" + s[:cl] + "```")


@client.command()
async def rps(ctx):
    if await hm.helpredirect(ctx, client): return
    opts = ["Rock", "Paper", "Scissors"]
    cmcs = ctx.message.content.split(" ")[1]
    rand = random.SystemRandom().randint(0,2)
    ic = opts[rand]
    win = ic + " wins!"
    if cmcs == "✊" or "rock" in cmcs.lower():
        if rand == 2: win = cmcs + " wins!"
        elif rand == 1: win = ic + " wins!"
        else: win = "It's a tie!"
    elif cmcs == "✂" or "scissors" in cmcs.lower():
        if rand == 1: win = cmcs + " wins!"
        elif rand == 0: win = ic + " wins!"
        else: win = "It's a tie!"
    elif cmcs == "📰" or "paper" in cmcs.lower():
        if rand == 0: win = cmcs + " wins!"
        elif rand == 2: win = ic + " wins!"
        else: win = "It's a tie!"
    else:
        new = opts[sum(ord(x) for x in ascii.__call__(cmcs)) % 3]
        if new == "Rock":
            if rand == 2: win = cmcs + " wins!"
            elif rand == 1: win = ic + " wins!"
            else: win = "It's a tie!"
        elif new == "Scissors":
            if rand == 1: win = cmcs + " wins!"
            elif rand == 0: win = ic + " wins!"
            else: win = "It's a tie!"
        elif new == "Paper":
            if rand == 0: win = cmcs + " wins!"
            elif rand == 2: win = ic + " wins!"
            else: win = "It's a tie!"
    await ctx.channel.send("You chose " + cmcs + ". I chose " + ic + ".\n" + win)
    
@client.command()
async def superrps(ctx):
    if await hm.helpredirect(ctx, client): return
    cmc = hm.cmc(ctx)
    if len(cmc) > 1: n = int(cmc[1])
    else: n = 25
    if n % 2 != 1:
        await ctx.send('We must have an odd number of "entrants"!')
        return
    file = open('dictionary.json', 'r+')
    dictionary = json.load(file)
    file.close()
    
    dic = list(dictionary.keys())
    rand = random.SystemRandom().randint(0, len(dic))
    myword = dic[rand].capitalize()
    mywordnum = sum(ord(x) for x in ascii.__call__(myword)) % n
    yourword = cmc[0].capitalize()[0] + cmc[0][1:].lower()
    yourwordnum = sum(ord(x) for x in ascii.__call__(yourword)) % n
    difference = (mywordnum - yourwordnum) % n
    halfn = (n-1)/2
    
    begin = f'I chose {myword}, you chose {yourword}.\n'
    if mywordnum == yourwordnum:
        await ctx.send(begin + 'It\'s a tie!')
    elif difference > halfn:
        await ctx.send(begin + f'{yourword} wins!')
    else:
        await ctx.send(begin + f'{myword} wins!')

@client.command()
async def emojify(ctx):
    if await hm.helpredirect(ctx, client): return
    author = ctx.author.name
    if author == "GoodAtBeingDerpy":
        author = "GABD"
    if len(author) > 8:
        author = author[:8] 
    stc = author + ": " + ctx.message.content.split(" ", 1)[1]
    
    links = []
    emojimen = []
    p = re.compile("https?:\\/\\/.+\\/")
    m = re.findall(p, stc)
    for x in m:
        links.append(x)
        stc = stc.replace(x, "⡈")
    links1 = iter(links)
    p = re.compile("<(?:\\:|@).*>")
    m = re.findall(p, stc)
    for x in m:
        emojimen.append(x)
        stc = stc.replace(x, "⡉")
    emojimen1 = iter(emojimen)
    
    s = "​"
    for x in stc:
        if x in asc:
            nrep = ord(x.lower())
            if x == " ":
                s += str(discord.utils.get(client.emojis, name="space", id=465069460588462090))
            elif nrep > 96 and nrep < 123:
                s += "​" + emojAN[nrep - 97] + "​"
            elif nrep > 47 and nrep < 58:
                s += emojAN[nrep - 22]
            elif x == "*":
                s += "*⃣"
            elif x == "!":
                s += "❗"
            elif x == "?":
                s += "❓"
            elif x == "#":
                s += "#⃣"
            elif x == ":":
                s += str(discord.utils.get(client.emojis, name="colon", id=465072882964365312))
            elif x == "-":
                s += "➖"
            elif x == "`":
                ""
            else:
                s += x
        elif x == "⡈":
            s += "<"+links1.__next__()+">"
        elif x == "⡉":
            s += emojimen1.__next__()
        else: s += x
    s = s.replace("​​​", "​").replace("​​", "​").replace("​\n", "\n").replace("\n​", "\n").strip()
    global mes_sageid
    mes_sageid = ctx.message.id
    await ctx.message.delete()
    await ctx.channel.send(s[:2000])
    
    
@client.command()
async def pfp(ctx):
    cmc = ctx.message.content.split(" ")[1:]
    if not cmc:
        user = ctx.author
    else: 
        user = hm.getmember(ctx.guild, cmc[0])
    byts = requests.get(user.avatar_url).content
    png = 'png' if '.gif' not in str(user.avatar_url) else 'gif'
#     print(user.avatar_url)
    if png == 'gif':
        await ctx.channel.send(user.avatar_url)
    else:
        file = io.BytesIO(byts)
        im = Image.open(file).convert('RGB')
        im.save(f'pfp.{png}', format=png)
        file.name = f'pfp.{png}'
        await ctx.channel.send(file=discord.File(f'pfp.{png}'))
    
    
@client.command()
async def rolecount(ctx):
    # if await hm.helpredirect(ctx, client): return
    cmc = hm.groupedsplit(ctx.message.content)[1:]
    if len(cmc) < 1:
        await ctx.channel.send(str(len(ctx.guild.roles)) + ' roles')
        return
    s = "​"
    for x in cmc:
        role = discord.utils.get(roles, name=x.replace("_", " "))
        if role:
            num = 0
            for y in ctx.guild.members:
                if role in y.roles:
                    num += 1
            s += "\n" + x.replace("_", " ") + ": " + str(num)
    if s != "​":
        await ctx.channel.send(s)
    
@client.command(pass_context = True)
async def graph(ctx):
#     updater = discord.utils.get(roles, name='Updater')
#     if not (ctx.message.channel.permissions_for(ctx.message.author).manage_roles or updater in ctx.message.author.roles):
#         await ctx.send('I\'ve recently decided that you don\'t have permission to use that command.')
#         return
#     todel = await ctx.send("May not be working atm.")
    cmc = ctx.message.content.split()[1:]
    top = not not cmc

    longestrole = 0
    for r in ctx.guild.roles:
        if len(str(r)) > longestrole:
            longestrole = len(str(r))
            
    strroles = []
    roles = []
    eb = []
    larnum = 0
    total = 0
    acf = []
    torev = []
    orderednums = []
    pos = 0
    for r in sorted(ctx.guild.roles, key=lambda x: x.position, reverse=True):
        if r.position <= 0:
            continue
        if pos == 0:
            pos = r.position
        num = 0
        if top:
            for m in r.members:
                if m.id not in acf:
                    num += 1
                    acf.append(m.id)
        else:
            num = len(r.members)
        if num:
            torev.append(str(r) + " "*((longestrole+1)-len(str(r))) + str(num))
            strroles.append(str(r))
            roles.append(r)
            eb.append(num)
            orderednums.append(pos)
            if num > larnum:
                larnum = num
            pos -= 1
            total += num
    for x in range(len(orderednums)):
        orderednums[x] = orderednums[x]-(pos-1)
        
    s = "```"
    corrected = reversed(torev)
    farmdict = {}
    counter = 0
    for x in corrected:
        s += x + "\n"
        
        num = x.split(" ")[-1]
        rank = ' '.join(x.split(" ")[:2])
        farmdict.update({counter: f'{num},{rank}'})
        counter += 1
    
    temptotal = 0
    halftotal = total//2
    temphalftotal = 0
    medianrank = ""
    for k, v in farmdict.items():
        numrank = v.split(',')
        num = int(numrank[0])
        temptotal += k * num
        temphalftotal += num
        if temphalftotal > halftotal and not medianrank:
            medianrank = numrank[1]
        
    avgrank = farmdict.get(temptotal//total).split(',')[1]
    s += f'Average: {avgrank}\n'
    s += f'Median: {medianrank}\n'
    
    s += "Total: " + str(total) + "```"
    "Finished making the string part of the return"
    
    orderednums = list(reversed(orderednums))
    eb = list(reversed(eb))
    if eb[0] > larnum: eb[0] = larnum
    strroles = list(reversed(strroles))
     
    #plt.subplots()
    #ax.yaxis.set_major_formatter(formatter)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    bars = plt.bar(orderednums, eb)
    plt.xticks(orderednums, strroles, rotation=45, va='baseline', ha='right', fontsize=9)
    plt.yticks(numpy.arange(-1, larnum+larnum//25, step=larnum//25), fontsize=9)
    colors = [str(x.colour) for x in reversed(roles)]
#     s = ''
#     for x in reversed(roles):
#         s += f'{x.name}: {x.colour}, '
#     print(s[:-2])
    for x in range(len(eb)):
        bars[x].set_color(colors[x])       
    ax.set_facecolor('#404040')
    tim = int(time.time())
    fig.savefig(f"graphs/graph{tim}.png", facecolor='#cccccc')
    plt.close(fig)
    await ctx.send(file=discord.File(f"graphs/graph{tim}.png"), content=s[:2000])
    #await todel.delete()
    "Finished making graph and sending everything"


@client.command()
async def memberrolelist(ctx):
    cmc = hm.groupedsplit(ctx.message.content)[1:]
    def getname(member):
        return member.name.lower()
    s = '```\n'
    for x in cmc:
        role = hm.getrole(ctx.guild, x)
        if role:
            s += f'{x.replace("_", " ")}:\n'
            for y in sorted(filter(lambda z: role in z.roles, ctx.guild.members), key=getname):
                s += f'{y.name}, '
            mems = s.count(', ')
            s = s[:-2]
            s += f' ({mems})'
    await ctx.channel.send(f'{s[:1990]}```')

@client.command()
async def assignroles(ctx):
    if await hm.noperms(ctx, 'manage_roles'):
        return
    cmc = hm.groupedsplit(ctx.message.content)[1:]
    roles = []
    members = []
    for x in cmc:
        role = hm.getrole(ctx.guild, x)
        if not role:
            member = hm.getmember(ctx.guild, x)
            if member: members.append(member)
        else: roles.append(role)
    for x in roles:
        for y in members:
            if x not in y.roles:
                await y.add_roles(x, atomic=False)
    await ctx.send('Success')

@client.command()
async def removeroles(ctx):
    if await hm.noperms(ctx, 'manage_roles'):
        return
    cmc = hm.groupedsplit(ctx.message.content)[1:]
    roles = []
    members = []
    for x in cmc:
        role = hm.getrole(ctx.guild, x)
        if not role:
            member = hm.getmember(ctx.guild, x)
            if member: members.append(member)
        else: roles.append(role)
    for x in roles:
        for y in members:
            if x in y.roles:
                await y.remove_roles(x, atomic=False)
    await ctx.send('Success')

@client.command()
async def calc(ctx):
    if await hm.helpredirect(ctx, client): return
    x = ctx.message.content.split(" ", 1)[1]
    await calc2(ctx.message, x)
    
async def calc2(message, x):
    calcgood = False
    op = "+-*/^%<<>>&|$↓↓:"
    rpldic = [(' ',''), ('openparenthesis','('), ('closeparenthesis',')'), ('closedparenthesis',')'),
            ('∞','infinity'), ('infinity','((2-(2^-52))*2^1023)'), ('centillion','*'+str(10**303)+''), ('nonagintillion', '*'+str(10**273)+''),
            ('octogintillion','*'+str(10**243)+''), ('septuagintillion','*'+str(10**213)+')'), ('sexagintillion','*'+str(10**183)+''),
            ('quinquagintillion','*'+str(10**153)+''), ('quadragintillion','*'+str(10**123)+''), ('trigintillion','*'+str(10**93)+''),
            ('vigintillion','*'+str(10**63)+''), ('decillion','*'+str(10**33)+')'), ('nonillion',str(10**30)+''), ('octillion','*'+str(10**27)+''), ('septillion','*'+str(10**24)+''),
            ('sextillion','*'+str(10**21)+''), ('quintillion','*'+str(10**18)+''), ('quadrillion','*'+str(10**15)+''), ('trillion','*'+str(10**12)+''),
            ('billion','*'+str(10**9)+''), ('million','*'+str(10**6)+''), ('thousand','*1000'), ('hundred','*100'),
            ('eighty','eightty'), ('teen','+10'), ('twelve','12'), ('eleven','11'), ('ten','10'),
            ('nine','+9'), ('eight','+8'), ('seven','+7'), ('six','+6'), ('five','+5'), ('four','+4'), ('three','+3'), ('two','+2'), ('one','+1'), ('zero','0'),
            ('plus','+'), ('minus','-'), ('negative','-'), ('times','*'), ('dividedby','/'), ('divide','/'), ('point','.'), ('tesseracted','^4'), ('cubed','^3'), ('squared','^2'),
            ('gross','*144'), ('dozen','*12'), ('score','*20'), ('naught','0'), ('none','0'), ('zip','0'), ('nada','0'),
            ('fif','+5'), ('for','+4'), ('thir','+3'), ('twen','+2'), ('ty','*10'), ('π','pi'), ('!','!1'), ('~','1~'),
            ('novem','*'+str(10**27)), ('octo','*'+str(10**24)), ('septen','*'+str(10**21)), ('sex','*'+str(10**18)), ('quin','*'+str(10**15)), ('quattour','*'+str(10**12)), ('tre','*'+str(10**9)),
            ('duo','*'+str(10**6)), ('trunc','tru_nc'), ('round','rou_nd'), ('un','*'+str(10**3)), ('rou_nd','round'), ('tru_nc','trunc'),
            (')(',')*('), ('randint(','ra_ndint('), ('rand(','ra_nd('), ('rand',str(random.random())), ('ra_nd(','rand(') , ('ra_ndint(', 'randint('),
            ('(+', '('), ('(*', '('), ('--', '+'), ('(.', '(0.'),
            ('++','+'), ('+*','+'), ('+/','/'), ('+%','%'), ('+-','-'), ('+^','^'), ('*+','*'), ('.+','.'),
            ('**','*'), ('/*','/'), ('/+','/'), ('%*','%'), ('-*','-'), ('^*','^'), ('<*','<'), ('>*','>'),
            ('-.','-0.'), ('*.', '*0.'), ('+.','+0.'), ('/.','/0.'), ('^.','^0.'),
            ('ans', hm.addprevcalc(str(message.author.id), ''))
            ]
    nsp = NumericStringParser()
    for y in x:
        if y in op + '!~':
            calcgood = True
            break
    for y in rpldic[1:]:
        if y[0] in x.replace(' ', '') or calcgood:
            calcgood = True
            break
    if not calcgood and '(' in x and ')' in x:
        calcgood = True
    
    line = x.replace(",", "")
    varis = hm.getprevvars(str(message.author.id))
    if '=' in x:
        count = 0
        for y in line.replace(', ', ' ').split(' '):
            if '=' not in y or '==' in y: 
                calcgood = True
                break 
            va = y.split('=')
            for k in list(varis.keys())[::-1]:
                va[1] = va[1].replace(k, varis[k])
#             va[1] = va[1].replace('ans', hm.addprevcalc(str(message.author.id), ''))
            try: result = await nsp.eval(va[1])
            except: continue
            try:
                if len(va[0])>0:
                    varis.update({va[0]:str(result)})
            except: return
            calcgood = False
            count += 1
        if count:
            line = ''.join(line.split(' ')[count:])
            hm.storeprevcalc(str(message.author.id), calc=None, vars=varis)
    if calcgood:
       
        if '//' in line:
            line = line[:line.find('//')]
        result = ""
        
        if len(line) == 0:
            return    
        if line[0] == '.':
            line = f'0{line}'
        if line[0] in op or line[:2] in op:
            line = hm.addprevcalc(str(message.author.id), line)
        for k in list(varis.keys())[::-1]:
            line2 = line.replace(k, varis[k])
        try:
            preeval = hm.wordnumtonum(line2, rpldic)
            print(preeval)
            result = await nsp.eval(preeval)
        except:
            line2 = hm.wordnumtonum(line, rpldic)
            for k in list(varis.keys())[::-1]:
                line = line.replace(k, varis[k])
                line2 = line
            try:
                result = await nsp.eval(line2, rpldic)
            except:
                if '==' in line and '==' not in line.replace('==', '', 1):
                    lr = line.split('==')
                    try:
                        r1 = await nsp.eval(hm.wordnumtonum(lr[0], rpldic))
                        r2 = await nsp.eval(hm.wordnumtonum(lr[1], rpldic))
                    except: return
                    else:
                        if r1 == r2:
                            await message.channel.send(f'True. {"{:,}".format(r1)} == {"{:,}".format(r2)}.'[:2000])
                        else:
                            await message.channel.send(f'False. {"{:,}".format(r1)} =/= {"{:,}".format(r2)}.'[:2000])
                        hm.storeprevcalc(str(message.author.id), str(r1))
        if (result or result == 0) and not str(result) == line.replace(' ', '') and not str(result) == line.replace("+", "", 1) and not str(result) == line.replace("-", "", 1):
            try:
                wholestrres = f'{str(result)}.'.split(".")[0]
                sendableresult = f'{str("{:,}".format(result))[:1987-len(str(len(str(wholestrres))))]}... ({len(str(wholestrres))} digits)' if len(str("{:,}".format(result))) > 2000 else f'{str("{:,}".format(result))[:1991-len(str(len(wholestrres)))]} ({len(wholestrres)} digits)' if len(wholestrres) > 9 else f'{str("{:,}".format(result))}'
                await message.channel.send(sendableresult)
            except:
                print(message.channel.id, message.channel.name)
            hm.storeprevcalc(str(message.author.id), str(result), vars=varis)


@client.command()
async def wa(ctx):
    if await hm.helpredirect(ctx, client): return
    cmc = ctx.message.content.split(' ', 1)[1]
    r = requests.get('http://api.wolframalpha.com/v1/result?appid=U7QXJX-VRAQKV8L5A&i=' + cmc)
    await ctx.channel.send(r.text)

def google_search(search_term, **kwargs):
    api_key = 'AIzaSyDK0pDZCPpaV90ubY1r14U-WZ50oSa0qqc'
    cse_id = '000888516484850439462:0msxuo3c30t'
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res['items']

@client.command()
async def wiki(ctx):
    if await hm.helpredirect(ctx, client): return
    results = google_search(' '.join(ctx.message.content.split(" ")[1:]) + " site:en.wikipedia.org", num=2)
    for x in results:
        await ctx.send(x['link'])
        break

@client.command()
async def search(ctx):
    if await hm.helpredirect(ctx, client): return
    cmc = ctx.message.content.split(' ')[1:]
    site = ''
    if '.' in cmc[0] and ':' not in cmc[0]:
        site = f' site:{cmc[0]}'
        cmc = cmc[1:]
    numres = 1
    if hm.integer(cmc[0]):
        numres = int(cmc[0])
        cmc = cmc[1:]
    tosearch = 10 if numres > 4 else numres*2
    results = google_search(' '.join(cmc) + site, num=tosearch)
    s = ''
    for idx, x in enumerate(results):
        if idx == numres:
            break
        if idx == 0:
            s += x['link'] + '\n'
            continue
        s += '<' + x['link'] + '>\n'
    await ctx.send(s)

@client.command()
async def palindrome(ctx):
    if await hm.helpredirect(ctx, client): return
    cmc = ctx.message.content.split(' ', 1)[1].lower().replace(' ', '')
    for x, y in zip(cmc, cmc[::-1]):
        if not x == y:
            await ctx.channel.send("No")
            return
    await ctx.channel.send("Yes")
    

@client.command()
async def dtm(ctx):
    if await hm.helpredirect(ctx, client): return
    cmc = ctx.message.content.split(" ", 2)[1:]
    if len(cmc) == 2:
        if hm.isdigit(cmc[1]):
            await ctx.channel.send((await client.get_channel(int(cmc[1])).fetch_message(int(cmc[0]))).jump_url)
        else: 
            await ctx.channel.send((await discord.utils.get(client.get_all_channels(), mention=cmc[1]).fetch_message(int(cmc[0]))).jump_url)
    elif len(cmc) == 1:
        await ctx.channel.send((await ctx.channel.fetch_message(int(cmc[0]))).jump_url)
    global mes_sageid
    mes_sageid = ctx.message.id
    await ctx.message.delete()
    
    
@client.command()
async def morse(ctx):
    if await hm.helpredirect(ctx, client): return
    cmc = ctx.message.content.replace(' / ', '/').replace('/', '  ').replace('//', '    ').upper().split(' ', 1)[1]
    morse = False
    for x in cmc:
        if x not in ".-/ '":
            morse = True
    if morse:
        await ctx.channel.send('```' + hm.texttomorse(cmc) + '```')
        return
    await ctx.channel.send('```' + hm.morsetotext(cmc) + '```')


@client.command()
async def invite(ctx):
    l = link.format(client.user.id)
    await ctx.channel.send(f"<{l}>")


@client.command()
async def wordcount(ctx):
    if await hm.helpredirect(ctx, client): return
    cmc = ctx.message.content.split(" ")[1:]
    after = None
    before = None
    target = None
    for x in range(0, len(cmc)):
        if cmc[x].lower() == "after":
            if hm.isdigit(cmc[x+1]):
                after = await ctx.channel.fetch_message(int(cmc[x+1]))
                if not after:
                    await ctx.channel.send("Invalid message id after after, perhaps you copied the user id instead of the message id?")
                    return
        elif cmc[x].lower() == "before":
            if hm.isdigit(cmc[x+1]):
                before = await ctx.channel.fetch_message(int(cmc[x+1]))
                if not before:
                    await ctx.channel.send("Invalid message id after before, perhaps you copied the user id instead of the message id?")
                    return
        elif not target:
            target = hm.gettarget(ctx, cmc[x])
    num = 0
    async for x in ctx.channel.history(limit=None, after=after, before=before):
        if x.author == target or target == None or target in x.author.roles:
            num += len(x.content) - len(x.content.replace(" ", "").replace("\n","")) + 1
    aftermsg = " after " + after.author.name + "'s specified message" if after else " before " + before.author.name + "'s specified message" if before else ""
    trg = target.name if target else "Everyone"
    await ctx.channel.send(trg + " has sent " + str(num) + " words in this channel"+ aftermsg +".")
    global mes_sageid
    mes_sageid = ctx.message.id
    await ctx.message.delete()
    
    
@client.command()
async def counting(ctx):
    global countingf
    cmc = ctx.message.content.split(" ")[1:]
    if not cmc:
        if not countingf:
            countingf = tilndb.counting.find_one()
        await ctx.send(countingf.get(str(ctx.guild.id)).get(str(ctx.channel.id)).get('current'))
        await ctx.message.delete()
        return
    if ctx.channel.permissions_for(ctx.author).manage_guild:
        
        #initialize variables
        channel = None
        increment = None
        start = None
        #arguments to variables
        for x in range(0, len(cmc)):
            if not channel:
                channel = hm.getchannel(ctx.guild, cmc[x])
                if channel:
                    continue
            if not increment:
                if cmc[x].lower() == 'off':
                    increment = 'off'
                    continue
                elif cmc[x][0] in '-+*^':
                    n = cmc[x][1:]
                    if hm.isdigit(n):
                        n = int(n) if int(n) == float(n) else float(n)
                        increment = cmc[x][0] + str(n)
                    else: 
                        await ctx.channel.send("Invalid increment.")
                        return
                    continue
            if not start:
                n = cmc[x]
                if hm.isdigit(n):
                    start = int(n) if int(n) == float(n) else float(n)
                    start = str(start)
                    continue
        #default values
        increment = '+1' if not increment else increment
        channel = ctx.channel if not channel else channel
        start = start if start else '0' if increment[0] in 'o+-' else '1' if increment[0] == '*' else '2'
        #load file
        if not countingf:
            countingf = tilndb.counting.find_one()
        #load dictionary
        gid = str(ctx.guild.id)
        gc = countingf.get(gid) or {}
        cid = str(channel.id)
        chanc = gc.get(cid) or {}
        #store in dictionary
        chanc.update({'inc':increment, 'current':start})
        gc.update({cid:chanc})
        countingf.update({gid:gc})
        #write to file
        tilndb.counting.replace_one({}, countingf)
        
        if ctx.channel.id in gc:
            await ctx.message.delete()
    else: await ctx.channel.send("You don't have permission to use that command.")
    

@client.command()
async def word(ctx):
    if await hm.helpredirect(ctx, client): return
    global haikuf
    if not haikuf:
        haikuf = tilndb.words.find_one()
    cmc = ctx.message.content.split(" ")[1:]
    
    exclude = set(string.punctuation.replace("'", ''))
    s = ''
    indict = False
    for x in range(len(cmc)):
        cmc[x] = ''.join(ch for ch in cmc[x] if ch not in exclude).upper()
        if cmc[x] in haikuf.keys() and not cmc[x].isdigit():
            s += f'{cmc[x]}: {haikuf[cmc[x]]}, '
            indict = True
        if not indict or str(ctx.author) == "Tiln#0416" or str(ctx.author) == "AndyVshr#1639" and not cmc[x].isdigit():
            nums = []
            for y in range(1, 10):
                try: num = int(cmc[x+y])
                except: break
                nums.append(str(num))
            if nums:
                s += 'changed to ' 
            for y in nums:
                s += y + ','
            if nums:
                s += '. '
                haikuf.update({cmc[x]: ','.join(nums)})
                tilndb.words.replace_one({}, haikuf)
    await ctx.send(s[:-2])
    
    
@client.command()
async def freedom(ctx):
    if await hm.noperms(ctx, 'manage_guild'):
        return
    servers = tilndb.freedom.find_one()
    sid = str(ctx.guild.id)
    server = servers.get(sid) or False
    server = not server
    servers.update({sid: server})
    tilndb.freedom.replace_one({}, servers)
    if server:
        await ctx.send("Freedom updated to true.")
    else:
        await ctx.send("Freedom updated to false.")
        
@client.command()
async def makeroleamuterole(ctx):
    if await hm.noperms(ctx, 'manage_roles'):
        return
    if await hm.helpredirect(ctx, client): return
    cmc = hm.groupedsplit(ctx.message.content)[1:]
    role = None
    undo = False
    for x in cmc:
        if x == 'undo':
            undo = True
        role = hm.getrole(ctx.guild, x)
        if role: break
    if not role: return
    if undo:
        ow = {'send_messages': None, 'speak': None, 'add_reactions': None}
    else:
        ow = {'send_messages': False, 'speak': False, 'add_reactions': False}
    for chan in ctx.guild.channels:
        try:
            overwrite = chan.overwrites_for(role)
            overwrite.update(**ow)
            await chan.set_permissions(role, overwrite=overwrite)
        except: pass

@client.command()
async def makeroleaninvisiblerole(ctx):
    if await hm.noperms(ctx, 'manage_roles'):
        return
    if await hm.helpredirect(ctx, client): return
    cmc = hm.groupedsplit(ctx.message.content)[1:]
    role = None
    undo = False
    for x in cmc:
        if x == 'undo':
            undo = True
        role = hm.getrole(ctx.guild, x)
        if role: break
    if not role: return
    if undo:
        ow = {'read_messages': None, 'send_messages': None, 'connect': None, 'add_reactions': None}
    else:
        ow = {'read_messages': False, 'send_messages': False, 'connect': False, 'add_reactions': False}
    for chan in ctx.guild.channels:
        try:
            overwrite = chan.overwrites_for(role)
            overwrite.update(**ow)
            await chan.set_permissions(role, overwrite=overwrite)
        except: 
            print(chan.name)
            pass


@client.command()
async def pin(ctx):
    global mes_sageid
    if await hm.noperms(ctx, 'manage_messages'):
        mes_sageid = ctx.message.id
        await ctx.message.delete()
        return
    pinned = False
    if len(ctx.message.content.split(" ")) > 1:
        mid = ctx.message.content.split(" ")[1]
        if hm.isdigit(mid):
            if int(mid) > 10000:
                msg = await ctx.channel.fetch_message(mid)
                await msg.pin()
                mes_sageid = ctx.message.id
                await ctx.message.delete()
                return
    async for x in ctx.channel.history():
        if ctx.message.mentions:
            if not x.content.startswith("!?pin") and x.author == ctx.message.mentions[0]:
                await x.pin()
                pinned = True
                break
        else:   
            if not x.content.startswith("!?pin"):
                await x.pin()
                pinned = True
                break
    if not pinned:
        await ctx.channel.send("The user you are trying to pin is not recent enough or does not exist.")
        await ctx.message.delete()

@client.command()
async def react(ctx):
    if await hm.noperms(ctx, 'add_reactions'):
        return
    if await hm.helpredirect(ctx, client): return
    global mes_sageid
    emojdup = [discord.utils.get(client.emojis, name="a_", id=448623901027860500), discord.utils.get(client.emojis, name="a_", id=485644541567959040), discord.utils.get(client.emojis, name="a_", id=448623554292875266), u'🅰', discord.utils.get(client.emojis, name="b_", id=448623288177000448), u'🅱', discord.utils.get(client.emojis, name="c_", id=448623288185257994), discord.utils.get(client.emojis, name="c_", id=448623554582282240), discord.utils.get(client.emojis, name="d_", id=448623287782604801), discord.utils.get(client.emojis, name="d_", id=448623900834922500), discord.utils.get(client.emojis, name="d_", id=448623554611773440), discord.utils.get(client.emojis, name="e_", id=448623554582282260), discord.utils.get(client.emojis, name="e_", id=448623980753190913), discord.utils.get(client.emojis, name="e_", id=448623288445435914), discord.utils.get(client.emojis, name="e_", id=448623900889186317), discord.utils.get(client.emojis, name="f_", id=448623288189714442), discord.utils.get(client.emojis, name="f_", id=448623554582544384), discord.utils.get(client.emojis, name="g_", id=448623554615836673), discord.utils.get(client.emojis, name="g_", id=448623288109891585), discord.utils.get(client.emojis, name="h_", id=448623554544664586), discord.utils.get(client.emojis, name="h_", id=448623288214880296), u'♓', discord.utils.get(client.emojis, name="i_", id=448623901040443392), discord.utils.get(client.emojis, name="i_", id=448623288277532692), discord.utils.get(client.emojis, name="i_", id=448623554611642368), u'ℹ', discord.utils.get(client.emojis, name="j_", id=448623287833198603), discord.utils.get(client.emojis, name="k_", id=448623288193646609), discord.utils.get(client.emojis, name="l_", id=448623901040443402), discord.utils.get(client.emojis, name="l_", id=448623554670362625), discord.utils.get(client.emojis, name="l_", id=448623288210686003), u'Ⓜ', u'♏', u'♍', discord.utils.get(client.emojis, name="n_", id=448623554628419584), discord.utils.get(client.emojis, name="n_", id=448623288197840926), u'♑', discord.utils.get(client.emojis, name="o_", id=448623288487247882), u'🅾', u'⭕', discord.utils.get(client.emojis, name="p_", id=448623288466276382), u'🅿', discord.utils.get(client.emojis, name="q_", id=448623288281726996), discord.utils.get(client.emojis, name="r_", id=448625035985420289), discord.utils.get(client.emojis, name="r_", id=448623287929667596), discord.utils.get(client.emojis, name="r_", id=448623900771745793), discord.utils.get(client.emojis, name="s_", id=448623554590932992), discord.utils.get(client.emojis, name="s_", id=448623288210554880), discord.utils.get(client.emojis, name="s_", id=448623901044375552), discord.utils.get(client.emojis, name="t_", id=448623287866490881), discord.utils.get(client.emojis, name="t_", id=448623901220536331), discord.utils.get(client.emojis, name="t_", id=448623980849659926), discord.utils.get(client.emojis, name="t_", id=448623554498527233), discord.utils.get(client.emojis, name="u_", id=448623554590933002), discord.utils.get(client.emojis, name="u_", id=448623288470601738), discord.utils.get(client.emojis, name="v_", id=448623288055496725), u'♈', discord.utils.get(client.emojis, name="w_", id=448623288214749187), discord.utils.get(client.emojis, name="w_", id=448623554519629825), '❎', '❌', discord.utils.get(client.emojis, name="y_", id=448623554636808193), discord.utils.get(client.emojis, name="y_", id=448623288210554900), discord.utils.get(client.emojis, name="z_", id=448623288512675840), u'❕', u'❔', u'✳', u'✖']
    doub = ["ab", "cl", "id", "ng", "ok", "vs", "wc", "!!", "!?", "new", "sos", "cool", "free"]
    dup = ["a", "a", "a", "a", "b", "b", "c", "c", "d", "d", "d", "e", "e", "e", "e", "f", "f", "g", "g", "h", "h", "h", "i", "i", "i", "i", "j", "k", "l", "l", "l", "m", "m", "m", "n", "n", "n", "o", "o", "o", "p", "p", "q", "r", "r", "r", "s", "s", "s", "t", "t", "t", "t", "u", "u", "v", "v", "w", "w", "x", "x", "y", "y", "z", "!", "?", "*", "*"]
    #dup = ["a", "b", "i", 'h', "m", "m", "m", "n", "o", "o", "p", "v", "x", "x", "!", "?", "*", "*"]
    duptrans = []
    cmc = ctx.message.content.split(" ")[1:]
    mes = None
    mem = None
    npstr = ''
    for x in cmc:
        if not mem:
            mem = hm.getmember(ctx.guild, x)
            if mem:
                continue
        if hm.isdigit(x) and not mes:
            if int(x) > 1000000000:
                try:
                    mes = await ctx.channel.fetch_message(int(x))
                    continue
                except: ""
        npstr += x + ' '
    npstr = npstr.strip()
    async for x in ctx.channel.history():
        if mes:
            x = mes
        if not mes and (x.content.startswith("!?react") or (mem and not x.author == mem)):
            continue
        emoji = []
        com = npstr
        for y in doub:
            if y in npstr.lower():
                doubemo = await hm.doub_char_to_emoji(y)
                com = com.replace(y, doubemo, 1)
        try:
            mes_sageid = ctx.message.id
            await ctx.message.delete()
        except: ""
        com = com.split(' ')
        npstr = npstr.split(' ')
        for y, u in zip(range(len(com)), npstr):
            mes = ""
            if u[0] == "<" and u[-1] == ">":
                mes = discord.utils.get(client.emojis, name=u.split(":")[1], id=int(u.split(":")[2][:-1]))
                if mes == None:
                    continue
            com[y] = com[y].lower()
            for z in doub:
                if z in com[y] and not mes:
                    doubemo = await hm.doub_char_to_emoji(z)
                    com[y] = com[y].replace(z, doubemo, 1)
                    doub.remove(z)
            if not mes and (len(com[y]) > 1 or com[y] in asc):
                for z in com[y]:
                    z = z.lower()
                    if z in asc:
                        nrep = ord(z)
                        if z in dup or z in duptrans:
                            if z in duptrans:
                                emoji.append(await hm.dup_char_to_emoji(z, dup, emojdup))
                                if z not in dup: duptrans.remove(z)
                                else: dup.remove(z)
                            else:
                                duptrans.append(z)
                                dup.remove(z)
                                if nrep == 33:
                                    emoji.append(emojmisc[1])
                                elif nrep == 63:
                                    emoji.append(emojmisc[2])
                                elif nrep == 42:
                                    emoji.append(emojmisc[5])
                                else:
                                    nrep -= 97
                                    emoji.append(emojAN[nrep])
                        elif nrep > 96 and nrep < 123:
                            nrep -= 97
                            emoji.append(emojAN[nrep])
                        elif nrep > 47 and nrep < 58:
                            nrep -= 22
                            emoji.append(emojAN[nrep])
                        elif nrep == 35:
                            emoji.append(emojmisc[0])
                        elif nrep == 43:
                            emoji.append(emojmisc[3])
                        elif nrep == 45:
                            emoji.append(emojmisc[4])
                        elif nrep == 47:
                            emoji.append(emojmisc[6])
                        elif nrep == 36:
                            emoji.append(emojmisc[7])
                    elif z in emojmisc or z in emojdoub:
                        emoji.append(z)
            elif mes:
                emoji.append(mes)
            else:
                emoji.append(com[y])
        for y in emoji[:20]:
            await x.add_reaction(y)
            await asyncio.sleep(0.02)
        return
#     await ctx.channel.send("The user you are trying to react to is not recent enough or does not exist.")
    mes_sageid = ctx.message.id
    await ctx.message.delete()
    
    
@client.command()
async def clearreactions(ctx):
    global mes_sageid
    if await hm.noperms(ctx, 'manage_messages'):
        mes_sageid = ctx.message.id
        await ctx.message.delete()
        return
    cmc = ctx.message.content.split(" ")[1:]
    mid = 0
    mem = ""
    if len(cmc) > 0:
        mid = cmc[0]
    if hm.isdigit(mid):
        if int(mid) > 100000000000000000:
            messsage = await ctx.channel.fetch_message(mid)
            await messsage.clear_reactions()
            mes_sageid = ctx.message.id
            await ctx.message.delete()
            return
        else:
            mid = int(mid)
    elif ctx.message.mentions:
        mem = ctx.message.mentions[0]
    num = 0
    async for x in ctx.channel.history():
        if not x.content == "!?clearreactions" and x.reactions and (x.author == mem or not mem):
            num += 1
            await x.clear_reactions()
            if num >= mid or not mid:
                break
    mes_sageid = ctx.message.id
    await ctx.message.delete()

@client.command()
async def cr(ctx):
    await cr2(ctx)
@client.command()
async def customresponses(ctx):
    await cr2(ctx)
async def cr2(ctx):
    if await hm.noperms(ctx, 'manage_messages', server=True):
        return
    if await hm.helpredirect(ctx, client): return
    global crf
    cmc = hm.groupedsplit(ctx.message.content.split(" ", 1)[1])
    if not crf:
        servers = tilndb.customresponses.find_one()
    else:
        servers = crf
    sid = str(ctx.guild.id)
    server = servers.get(sid) or {}
    opts = ['ci', 're', 'd', 'dm', 'ss', 'sw', 'sss', 'ssw', 'own', 'adm', 'ms', 'mr', 'mc', 'km', 'bm', 'mn', 'mm', 
            'me', 'bot', '!own', '!adm', '!ms', '!mr', '!mc', '!km', '!bm', '!mn', '!mm', '!me', '!bot']
    selfopts = []
    cmc2 = []
    for x in cmc:
        x = x.replace('\\n', '\n').replace(r'\`', '`')
        if x in opts:
            selfopts.append(x)
        elif x.endswith('%'):
            try:
                num = int(x[:-1])
                if num <= 100 and num >= 0:
                    selfopts.append(str(num)+'%')
                else:
                    cmc2.append(x) 
            except: cmc2.append(x)
        elif x[-7:] == 'seconds' and ' ' not in x[:-7] and hm.isdigit(x[:-7]):
            selfopts.append(x)
        else:
            cmc2.append(x) 

    responses = cmc2[1:] if len(cmc2) > 2 else [cmc2[1]] if len(cmc2) == 2 else []
    if not len(responses) and not len(selfopts):
        server.pop(cmc2[0])
    else:
        server.update({cmc2[0]:[selfopts, responses]})
    servers.update({sid: server})
    tilndb.customresponses.replace_one({}, servers)
    crf = servers
    await ctx.send("Success")

@client.command()
async def editcustomresponseoptions(ctx):
    if await hm.noperms(ctx, 'manage_messages', 'manage_roles'):
        return
    if await hm.helpredirect(ctx, client): return
    cmc = hm.groupedsplit(ctx.message.content.split(" ", 1)[1])
    servers = tilndb.customresponses.find_one()
    sid = str(ctx.guild.id)
    server = servers.get(sid) or {}
    
@client.command()
async def lcr(ctx):
    await lcr2(ctx)
@client.command()
async def listcustomresponses(ctx):
    await lcr2(ctx)
async def lcr2(ctx):
    if await hm.noperms(ctx, 'manage_messages', server=True):
        return
    servers = tilndb.customresponses.find_one()
    sid = str(ctx.guild.id)
    server = servers.get(sid) or {}
    
    cmc = hm.groupedsplit(ctx.message.content.split(" ", 1)[1:])
    if len(cmc) and cmc[0] in server.keys():
        opre = server[cmc[0]]
        opres = ''
        for x in opre:
            for y in x:
                y = y.replace("\n", "\\n").replace('`', r'\`')
                opres += f' "{y}"' if ' ' in y else f' {y}'
        s = '```\n'
        s += f'{hm.getprefix(ctx.guild.id)}cr "{cmc[0]}"{opres}```'
        await ctx.send(s)
        return
    
    s = '```'
    invocations = '```'
    for k, v in server.items():
        k = k.replace("\n", "\\n").replace('`', r'\`')
        invocations += k + '\n'
        s += f'\n\n"{k}":'
        #[" " + str(a) + "" for a in v]
        for x in v:
            for y in x:
                y = y.replace("\n", "\\n").replace('`', r'\`')
                s += f' "{y}"' if ' ' in y else f' {y}'
    if len(s) < 1997:
        await ctx.send(s[:3] + s[4:] + '```')
    else:
        file = open('message.txt', 'w+', encoding='UTF-8')
        file.write(s[:3] + s[4:] + '```')
        file.close()
        file = open('message.txt', 'rb')
        await ctx.send(invocations + '```', file=discord.File(file))
        file.close()
    
@client.command()
async def cro(ctx):
    if await hm.noperms(ctx, 'manage_messages', server=True):
        return
    descs = ['caseInsensitive', 'regex', 'delete', 'direct-message', 'substring', 'subword', 
             'separatedSubstring', 'separatedSubword', 'owner', 'admin', 'manageServer', 'manageRoles', 'manageChannels', 
             'kickMembers', 'banMembers', 'manageNicknames', 'manageMessages', 'mentionEveryone', 'bot', 'notOwner', 
             'notAdmin', 'notManageServer', 'notManageRoles', 'notManageChannels', 'notKickMembers', 'notBanMembers', 
             'notManageNicknames', 'notManageMessages', 'notMentionEveryone', 'notBot', '%ChanceToDo(as 50%)', 
             'delay(Seconds, as 15seconds)']
    opts = ['ci', 're', 'd', 'dm', 'ss', 'sw', 'sss', 'ssw', 'own', 'adm', 'ms', 'mr', 'mc', 'km', 'bm', 'mn', 'mm', 'me', 'bot', '!own', '!adm', '!ms', '!mr', '!mc', '!km', '!bm', '!mn', '!mm', '!me', '!bot', '​', '​']
    s = '```'
    for x, y in zip(opts, descs):
        s += f'\n{x}: {y}'
    await ctx.send(s + '```')

@client.command()
async def convert(ctx):
    if await hm.helpredirect(ctx, client): return
    basedict = {
        '2' : '01', '3' : '012', '4' : '0123', '5' : '01234', '6' : '012345', '7' : '0123456', '8' : '01234567', '9' : '012345678',
        '10' : '0123456789', '11' : '0123456789a', '12' : '0123456789ab', '13' : '0123456789abc', '14' : '0123456789abcd', '15' : '0123456789abcde',
        '16' : '0123456789abcdef', '17' : '0123456789abcdefg', '18' : '0123456789abcdefgh', '19' : '0123456789abcdefghi', '20' : '0123456789abcdefghij',
        '21' : '0123456789abcdefghijk', '22' : '0123456789abcdefghijkl', '23' : '0123456789abcdefghijklm', '24' : '0123456789abcdefghijklmn',
        '25' : '0123456789abcdefghijklmno', '26' : '0123456789abcdefghijklmnop', '27' : '0123456789abcdefghijklmnopq', '28' : '0123456789abcdefghijklmnopqr',
        '29' : '0123456789abcdefghijklmnopqrs', '30' : '0123456789abcdefghijklmnopqrst', '31' : '0123456789abcdefghijklmnopqrstu',
        '32' : '0123456789abcdefghijklmnopqrstuv', '33' : '0123456789abcdefghijklmnopqrstuvw', '34' : '0123456789abcdefghijklmnopqrstuvwx',
        '35' : '0123456789abcdefghijklmnopqrstuvwxy', '36' : '0123456789abcdefghijklmnopqrstuvwxyz', 'allow' : ' abcdefghijklmnopqrstuvwxyz',
        'allup' : ' ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'alpha' : ' abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', '60' : '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwx',
        '62' : '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz', '64' : '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_-',
        'ascii': '                                 !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~                                  ¡¢£¤¥¦§¨©ª«¬­®¯°±²³´µ¶·¸¹º»¼½¾¿ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿ',
        '65536' : '65536', 'time' : ['00','01','02','03','04','05','06','07','08','09',10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59]
        }
    cmc = ctx.message.content.replace(',', '').split(' ')[1:]
    
    inp = ""
    source = ""
    target = ""
    for x in cmc:
        if x in basedict.keys() and not source:
            source = basedict[x]
        elif x in basedict.keys() and not target:
            target = basedict[x]
        else:
            inp += f'{x} '
    if not target:
        await ctx.send("No target specified")
        return
    noUps = True
    for x in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        if x in source:
            noUps = False
            break
    if noUps:
        inp = inp.lower()
    inp = inp[:-1]
    if ' ' not in inp:
        await ctx.send(hm.convert(inp, source, target))
    else:
        s = ''
        for x in hm.groupedsplit(inp):
            s += hm.convert(x, source, target) + ' '
        if len(s) < 2001:
            await ctx.send(s[:-1])
        else:
            file = open('message.txt', 'w+')
            file.write(s)
            await ctx.send(file=discord.File(file))
            file.close()
            
@client.command()
async def trim(ctx):
    if await hm.helpredirect(ctx, client): return
    cmc = ctx.message.content.split(" ")[1:]
    await ctx.send(''.join(cmc))
    
@client.command()
async def echo(ctx):
    updater = discord.utils.get(roles, id=455394098753437706)
    polls = discord.utils.get(roles, id=467349295532736512)
    nop = await hm.noperms(ctx,'manage_messages', send=False, server=True)
    if nop:
        if updater not in ctx.author.roles and polls not in ctx.author.roles:
            await ctx.send(nop)
            return
    if await hm.helpredirect(ctx, client): return
    cmc = ctx.message.content.split(" ")[1:]
    cmc = [x for x in cmc if len(x) != 0]
    targets = []
    chan = ""
    torem = ""
    for y in range(len(cmc)):
        x = cmc[y]
        if x[0] == '{' and x[-1] == '}':
            if ctx.channel.permissions_for(ctx.author).manage_messages or updater in ctx.message.author.roles:
                target = hm.gettarget(ctx, x[1:-1])
                cmc[y] = target.mention
                if not type(target) == discord.User and not type(target) == discord.Member:
                    targets.append(target)
        elif not chan:
            chan = hm.getchannel(ctx.guild, x)
            if chan:
                torem = x
                break
    for x in targets:
        if x.mentionable:
            targets.remove(x)
        else:
            await x.edit(mentionable = True)
    if ctx.channel.permissions_for(ctx.author).mention_everyone and not hm.cmddisabled(str(ctx.guild.id), 'someone'):
        mems = ctx.channel.members
        mems.remove(ctx.author)
        cmc = ' '.join(cmc).replace('@someone', mems[random.SystemRandom().randint(0, (len(mems)-1))].mention).split(' ')
    if chan:
        if chan.permissions_for(ctx.author).send_messages:
            cmc.remove(torem)
            await chan.send(' '.join(cmc).replace('\\n', '\n'))
        else: await ctx.send("No.")
    else:
        await ctx.send(' '.join(cmc).replace('\\n', '\n'))
    global mes_sageid
    mes_sageid = ctx.message.id
    await ctx.message.delete()
    await asyncio.sleep(2)
    for x in targets:
        await x.edit(mentionable = False)
        
@client.command()
async def embedize(ctx):
    if await hm.helpredirect(ctx, client): return
    cmc = hm.groupedsplit(ctx.message.content)[1:]
    
    chan = None
    mes = None
    title = ''
    footer = ''
    for x in cmc:
        if not chan:
            chan = hm.getchannel(ctx.guild, cmc)
            if chan: continue
        if hm.integer(x) and not mes:
            try:
                mes = await (chan or ctx.channel).fetch_message(int(x))
                continue
            except: pass
        if not title:
            title = x
            continue
        if not footer:
            footer = x
            continue
    if not mes: return
    embed = discord.Embed(title=title, description=mes.content,  timestamp=mes.created_at, url=mes.jump_url)
    embed.set_footer(text=footer)
    embed.set_author(name=mes.author.name, icon_url=mes.author.avatar_url)
    await ctx.send(embed=embed)
        
@client.command()
async def thewave(ctx):
    if await hm.helpredirect(ctx, client): return
    cmc = [int(x) for x in ctx.message.content.split(' ', 1)[1:]]
    while len(cmc) < 2:
        cmc.append(5)
    msgs = []
    for x in range(cmc[0]%100):
        msg = await ctx.send(r"\_ "*(x+1))
        msgs.append(msg)
        await asyncio.sleep(.2)
#     for _11 in range(cmc[1]):
#         await msgs.pop(0).delete()
#         msg = await ctx.send("Wave")
#         msgs.append(msg)
    await ctx.message.delete()
    for _11 in range(len(msgs)):
        await msgs.pop(0).delete()
        await asyncio.sleep(.2)
        
@client.command()
async def mountains(ctx):
    '''
    Base block
    Peak size
    Peaks
    Prominence(absolute or relative)
    Grade of the Mountain Range
    Grade of the Mountains
    Randomness
    '''
    if await hm.helpredirect(ctx, client): return
    cmc = hm.groupedsplit(ctx.message.content)[1:]
    base = '_ '
    ints = []
    for x in cmc:
        try:
            ints.append(int(x))
        except:
            base = x
            continue
    while(len(ints) < 2):
        ints.append(5)
    if len(ints) < 3:
        ints.append(ints[0]-1)
    if len(ints) < 4:
        ints.append(1)
    invprom = ints[0]-ints[2]
    valley = ints[2]-ints[0]
    s = f'\n{invprom*base}\n' 
    for x in range(ints[1]):
        for y in list(range(invprom+1, ints[0]))+list(range(ints[0], invprom-1, -1)):
            if y < 0:
                s += (valley+y)*' '*len(base) + base*(-y) + '\n'
            else:
                s += valley*' '*len(base) + base*y + '\n'
    await ctx.send(f'{s}')
    
@client.command()
async def renamealltherolesyesimabsolutelysure(ctx):
    if not ctx.channel.permissions_for(ctx.author).manage_roles:
        return
    
    for x in ctx.guild.roles:
        try: await x.edit(name='')
        except: continue

@client.command()
async def createtheroles(ctx):
    if not ctx.channel.permissions_for(ctx.author).manage_roles:
        return
    if await hm.helpredirect(ctx, client): return
    cmc = hm.groupedsplit(ctx.message.content)[1:]
    
    for x in cmc:
        await ctx.guild.create_role(name=x)

@client.command()
async def givemeeveryrole(ctx):
    if not ctx.channel.permissions_for(ctx.author).manage_roles:
        return
    rolestogive = [x for x in ctx.guild.roles if x not in ctx.author.roles]
    await ctx.author.add_roles(*rolestogive)
    
@client.command()
async def rainbowizetheroles(ctx):
    if await hm.noperms(ctx, 'manage_roles'):
        return
    if await hm.helpredirect(ctx, client): return
    cmc = hm.groupedsplit(ctx.message.content)[1:]
    if len(cmc) < 2:
        return
    
    startingRole = None
    reverse = False
    nums = None
    huerange = None
    for x in cmc:
        if x == 'reverse':
            reverse = True
            continue
        if not startingRole:
            startingRole = hm.getrole(ctx.guild, x)
            if startingRole: continue
        if hm.integer(x):
            nums = int(x)
            continue
        if '-' in x and [hm.integer(y) for y in x.split('-')] == [True, True]:
            rns = [int(y) for y in x.split('-')]
            if rns[0] >= 0 and rns[0] < 360 and rns[1] >= 0 and rns[1] < 360:
                huerange = rns
            
            
    if not startingRole or not nums or not huerange:
        print(startingRole, nums, huerange)
        return

    offset = -numpy.pi/2 - 2*numpy.pi*(60/360)
    x = numpy.linspace(offset, 2 * numpy.pi + offset, 360)
    sinewave = list(numpy.sin(x))
    
    offset = 0
    if huerange[1] - huerange[0] < 0:
        offset = 360-huerange[0]
        huerange[1] += offset
        hues = [int(x+0.5) for x in numpy.linspace(0, huerange[1], nums)]
#         hues = list(range(0, huerange[1]+huerange[1]//nums, huerange[1]//nums))
        hues = [hm.mod(x-offset, 360) for x in hues]
        '300-60 -> 0-120 w/offset@-60 -> 300-359,0-60'
    else:
        hues = [int(x+0.5) for x in numpy.linspace(huerange[0], huerange[1], nums)]
    rgbs = []
    for x in hues:
        lightness = 50
        saturation = 100
        sine = sinewave[x]
        if sine < 0:
            lightness += 12*sine
        if sine > 0:
            idc = 24*sine
            saturation -= idc
            lightness += idc/2
        hue = x/360
        lightness = lightness/100
        saturation = saturation/100
        rgb = [int(y*255+0.9) for y in colorsys.hls_to_rgb(hue, lightness, saturation)]
        rgbs.append(rgb)
    if reverse: rgbs = reversed(rgbs)
    rolesupdated = await ctx.guild.fetch_roles()
    for idx, x in enumerate(rgbs):
        role = discord.utils.get(rolesupdated, position=startingRole.position+idx)
        await role.edit(color=discord.Colour.from_rgb(*x))
    
@client.command()
async def gethexcodes(ctx):
    if await hm.helpredirect(ctx, client): return
    cmc = ctx.message.content.split(' ', 1)[1:]
    s = ''
    if cmc[0] == 'all':
        theroles = ctx.guild.roles
    elif hm.getmember(ctx.guild, cmc[0]):
        theroles = hm.getmember(ctx.guild, cmc[0]).roles
    else:
        theroles = ctx.author.roles
    strroles = []
    roles = []
    for x in theroles:
        rgb = [str(hex(a))[2:] for a in x.color.to_rgb()]
        hexx = ''.join(['0'*(2-len(a)) + a for a in rgb])
        if hexx != '000000':
            strroles.append(x.name)
            roles.append(x)
            s += f'{x.name}: #{hexx} <https://www.color-hex.com/color/{hexx}>\n'
    if s:
        orderednums = [x for x in range(len(strroles))]
        eb = [10 for x in range(len(strroles))]
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        bars = plt.bar(orderednums, eb)
        plt.xticks(orderednums, strroles, rotation=45, va='baseline', ha='right', fontsize=9)
        plt.yticks(numpy.arange(-1, 10, step=1), fontsize=9)
        colors = [str(x.colour) for x in roles]
        for x in range(len(eb)):
            bars[x].set_color(colors[x])       
        ax.set_facecolor('#404040')
        tim = int(time.time())
        fig.savefig(f"graphs/graph{tim}.png", facecolor='#cccccc')
        plt.close(fig)
        
        
        splitres = s.split('\n')
        tempres = ""
        for x in range(len(splitres)-1):
            tempres += splitres[x] + '\n'
            if len(tempres + splitres[x+1]) > 2000:
                await ctx.send(tempres[:-1])
                tempres = ""
        await ctx.send(file=discord.File(f"graphs/graph{tim}.png"), content=tempres[:2000])
        
@client.command()
async def cat(ctx):
    await ctx.send(json.loads(requests.get('http://aws.random.cat/meow').content).get('file'))
@client.command()
async def catsays(ctx):
    if await hm.helpredirect(ctx, client): return
    resp = requests.get(f'https://cataas.com/cat/says/{ctx.message.content.split(" ", 1)[1]}')
    byts = resp.content
    file = io.BytesIO(byts)
    fname = 'cat.' + resp.headers.get('Content-Type').split('/',1)[1]
#     fname = re.findall("filename=(.+)", d)
    file.name = fname
    await ctx.send(file=discord.File(file))        

@client.command()
async def length(ctx):
    if await hm.helpredirect(ctx, client): return
    cmc = ctx.message.content.split(" ", 1)[1]
    await ctx.send(len(cmc))

@client.command()
async def waketilnup(ctx):
    cmc = ctx.message.content.split(" ", 1)[1]
    voice = tts.sapi.Sapi()
    voice.create_recording('tts.wav', cmc)

    sd.default.device = 6
    numpyAudioArray = numpy.array(read("tts.wav")[1])
    sd.play(numpyAudioArray, 22050)

@client.command()
async def tellbotter(ctx):
    if await hm.helpredirect(ctx, client): return
    cmc = ctx.message.content.split(" ")[1:]
    if not cmc:
        return
    botter = client.get_user(115707766714138627)
    await botter.send(str(ctx.author) + ': ' + ' '.join(cmc))

@client.command()
async def dm(ctx):
    if await hm.helpredirect(ctx, client): return
    cmc = ctx.message.content.split(" ")[1:]
    target = None
    guild = None
    text = ''
    for x in cmc:
        if not guild:
            guild = hm.getguild(client, x)
            if guild:
                continue
        if not target:
            target = hm.getmember((guild or ctx.guild), x)
            if target:
                continue
        text += x + ' '
    if not target:
        try:
            target = await client.get_user(int(cmc[0]))
        except: return
    try:
        await target.send(str(ctx.author) + ': ' + text.strip())
    except:
        print(f'cannot send message to {ctx.author}')
    
async def enrf2(ctx, d=False):
    if await hm.helpredirect(ctx, client): return
    global enrf
    cmc = ctx.message.content.split(" ")[1:]
    target = None
    channel = None
    guild = None
    for x in cmc:
        if not guild:
            guild = hm.getguild(client, x)
            continue
        if guild:
            channel = hm.getchannel(guild, x)
            if channel != None:
                break
        if guild:
            target = hm.getmember(guild, x)
            break
    if not channel.name == 'echonreturnfirst':
        nop = await hm.noperms(ctx,'manage_messages', send=False, server=True)
        if nop:
            await ctx.send(nop)
            return
    try:
        if channel:
            if ctx.author.id not in [x.id for x in channel.members] and not ctx.author.bot and not channel.name == 'echonreturnfirst':
                #print(ctx.author, channel.name, channel.members, ctx.author.id)
                await ctx.send("I cannot send this because you are not a member of the target channel.")
                return
            await channel.send(' '.join(cmc[2:]))
        elif target:
            await target.send(' '.join(cmc[2:]))
        else:
            return
    except: return
    if d:
        try: await ctx.message.delete()
        except: pass
    if channel:
        enrf.update({channel.id: [ctx.guild.id, ctx.channel.id, ' '.join(cmc[2:])]})
    elif target:
        enrf.update({target.dm_channel.id: [ctx.guild.id, ctx.channel.id, ' '.join(cmc[2:])]})
    
@client.command()
async def echonreturnfirst(ctx):
    await enrf2(ctx)
    
@client.command()
async def echonreturnfirstd(ctx):
    await enrf2(ctx, True)

# @client.command()
# async def replace(ctx):
#     if str(ctx.author) != "Tiln#0416":
#         return
#     cmc = ctx.message.content.split(" ")[1:].split("|")
#     message = await ctx.channel.fetch_message(int(cmc[0]))
#     cmc = cmc[1:]
#     if cmc[0] in message.content:
#         await message.edit(content=message.content.replace(cmc[0], cmc[1]))
# #     for x in range(len(cmc)):
# #         if cmc[x] in message.content:

@client.command()
async def givereadaccess(ctx):
    if hm.noperms(ctx, 'manage_roles'):
        return
    if await hm.helpredirect(ctx, client): return
    cmc = hm.groupedsplit(ctx.message.content.split(' ', 1)[1])
    overwrite = discord.PermissionOverwrite(read_messages=True)
    for x in cmc:
        role = hm.getrole(ctx.guild, x)
        if not role: print(x)
        else:
            await ctx.channel.set_permissions(role, overwrite=overwrite)
    await ctx.message.delete()
    
@client.command()
async def listroles(ctx):
    if await hm.noperms(ctx, 'manage_roles'):
        return
    s = ''
    for x in ctx.guild.roles:
        s += f'"{x.name}" '
    await ctx.send(s)

# @client.command()
# async def streaming(ctx):
#     s = ''
#     for x in ctx.guild.members:
#         if x.activity != None and x.activity.type != 4 and str(x.activity.type) == "ActivityType.streaming":
#             s += f'`{x.name}` is playing `{x.activity.game}` - `{x.activity.details}`. <{x.activity.url}>\n'
#     if s:
#         await ctx.send(s)
#     else:
#         await ctx.send('No one is streaming in this server.')


@client.command()
async def shrug(ctx):
    await ctx.send(r"¯\\\_(ツ)\_/¯")
    
@client.command()
async def annoyingspoilerization(ctx):
    if await hm.helpredirect(ctx, client): return
    cmc = ctx.message.content.split(" ", 1)[1]
    cmc = cmc.replace(r'\|', '|').replace('|', r'\|')
    s = ""
    for x in cmc:
        s += f'||{x}||'
    while len(s) > 2000 or (len(s) - len(s.replace(r'|', '')) - (len(s) - len(s.replace(r'\|', '')))) % 4 != 0:
        s = s[:-1]
    await ctx.send(s)
    await ctx.message.delete()
    
@client.command()
async def units(ctx):
    cmc = ctx.message.content.split(" ")[1:]
    try: num = float(cmc[0])
    except: return
    try: 
        result = eval(f'num * unit_registry(cmc[1])')
        result = eval(f'result.to(cmc[2])')
    except Exception as e:
        await ctx.send(e)
        return
    if float(str(result).split()[0]) != 1.00:
        result = str(result) + 's'
    result = result.split()[0] + ' `' + result.split(' ', 1)[1] + '`'
    await ctx.send(result)

@client.command()
async def ctof(ctx):
    if await hm.helpredirect(ctx, client): return
    cmc = ctx.message.content.split(" ", 1)[1]
    await ctx.send(float(cmc)*(9/5)+32)

@client.command()
async def ftoc(ctx):
    if await hm.helpredirect(ctx, client): return
    cmc = ctx.message.content.split(" ", 1)[1]
    await ctx.send((float(cmc)-32)*(5/9))
    
@client.command()
async def improvedhardening(ctx):
    healths = ctx.message.content.split()[1:]
    h = []
    for x in healths:
        try: h.append(int(x))
        except: continue
    if len(h) < 2: return
    boostedhealth = max(h)
    basehealth = min(h)

    ad = hm.bracesplit(ctx.message.content, ('[',']'))[1][0]
    alphadist = []
    for x in ad.split(', '):
        try: alphadist.append(int(x))
        except: continue

    alphas = set(alphadist)
    minmax = {}
    for x in alphas:
        minmax.update({x:(int(x*0.75+0.5), int(x*1.25+0.5))})

    totboostwins = 0
    totshots = 0
    lm1 = len(alphadist)-1
    rng = numpy.random.default_rng()
    await ctx.channel.trigger_typing()
    for x in range(1, 100001):
        health = boostedhealth
        while(health) > 0:
            if health <= boostedhealth-basehealth:
                totboostwins += 1
            alpha = alphadist[randint(0, lm1)]
            sub = int(rng.normal(alpha, alpha/8)+0.5)
            mini = minmax[alpha][0]
            maxi = minmax[alpha][1]
            if sub < mini: sub = mini
            elif sub > maxi: sub = maxi
            health -= sub
            totshots += 1
    tot = 100000
    s = f'With {basehealth} base health and {boostedhealth} boosted health, defending against these alphas: {str(alphadist)[1:-1]}, there is a {round(totboostwins/tot*100)}% chance you\'d take an extra hit. This raises the average hits taken from {round((totshots-totboostwins)/x, 1)} to {round(totshots/x, 1)}, giving an effective health increase of {round((totshots/(totshots-totboostwins)-1)*100, 1)}%.\nSimulated with 100,000 trials, randomly picking among the given alphas for each shot, and fully simulating the rng of each shot, as per WoT\'s specifications.'
    await ctx.send(s)

# @client.command()
# async def srcname(ctx):
#     name = ctx.message.content.split(" ")[1]
#     srcnames = json.load(open('jsons/srcnames.json', 'r+'))
    
@client.command()
async def linkstogames(ctx):
    if await hm.helpredirect(ctx, client): return
    cmc = ctx.message.content.split(' ')[1:]
    
    games = []
    paragraphss = []
    async for x in hm.getchannel(ctx.guild, cmc[0]).history(limit=None):
        rp = re.compile(r"((?:https?:\/\/)?(?:www\.)?[A-Za-z0-9]{1,}\.(?:(?:com)|(?:net)|(?:org)|(?:tv))[A-Z|a-z|\-|_|=|?|0-9|\/|\.]{1,})")
        m = re.findall(rp, x.content)
        for y in m:
            if 'speedrun' in y:
                resp = requests.get(y)
                s = ""
                s += "<" + y + ">\n"
                paragraphs = justext.justext(resp.content, justext.get_stoplist("English"))
                paragraphss.append(paragraphs)
            else: print('else:', y)
    for idx, pgraphs in enumerate(paragraphss):
        for w, y in enumerate(pgraphs):
            if (w < len(pgraphs) - 2 and idx < len(paragraphss) - 2 and 
             y.text != paragraphss[idx+1][w].text and y.text != paragraphss[idx+2][w].text) or ( 
             w > 2 and idx > 2 and 
             y.text != paragraphss[idx-1][w].text and y.text != paragraphss[idx-2][w].text):
                try:
                    year = int(pgraphs[w+1].text)
                    plats = pgraphs[w+2].text
                except: 
                    try:
                        year = int(pgraphs[w+2].text)
                        plats = pgraphs[w+3].text
                    except: continue
                game = pgraphs[w].text
                if '(' in game and ')' in game and (plat := game[game.index('(')+1:game.index(')')]) in plats:
                    game = game.replace(f' ({plat})', '')
                plats = f' ({plats})'
                if f' ({year})' in game: game = game.replace(f' ({year})', '')
                if game != 'Error' and f'{game}{plats}' not in games:
                    games.append(f'{game}{plats}')
                break
    s = ''
    s2 = ''
    games = sorted(games, key=lambda s: s.lower())
    for x in range(len(games)):
        s += f'{emojAN[x]} {games[x]}\n'
        s2 += f'"{games[x]}" '
    s = s[:-1] 
    await ctx.send(s[:2000])
    await ctx.send(s2[:2000])
    
@client.command()
async def binompdf(ctx):
    cmc = hm.cmc(ctx)
    try:
        n = int(cmc[0])
        P = float(cmc[1])
        x = int(cmc[2])
    except: return
    await ctx.send(f'{(((n*(n+1))/2) / ((x*(x+1))/2)) * P**x * (1-P)**(n-x)}')

@client.command()
async def reducemyarray(ctx):
    if await hm.helpredirect(ctx, client): return
    c = hm.bracesplit(ctx.message.content, ('[', ']'))
    cmc = c[2][0].split(' ')[1:]
    newsize = 0
    trunc = False
    for x in cmc:
        if hm.integer(x):
            newsize = int(x)
        elif x == 'trunc':
            trunc = True
    arrays = c[1]
    ats = ctx.message.attachments
    for x in ats:
        byts = await x.read()
        arrays.append(byts.decode('utf-8'))
    for x in arrays:
        if x[0] != '[':
            x = '[' + x
        if x[-1] != ']':
            x = x + ']'
        for y in x:
            if y not in '[]0123456789 ,.':
                return
        nums = eval(x)
        averagingsize = len(nums) // newsize
        newarray = []
        leftover = len(nums) % averagingsize
        if leftover:
            leftovers = sum(nums[-leftover:-1]) / leftover
        for y in range(0, len(nums)-averagingsize-leftover, averagingsize):
            total = 0
            for z in range(averagingsize):
                total += nums[y+z]
            newarray.append(total/averagingsize)
        if leftover:
            newarray[-1] = (newarray[-1] + leftovers) / 2
        if trunc:
            newarray = [int(x) for x in newarray]
        result = str(newarray)
        result = result.replace(',', '')
        if len(result) <= 2000:
            await ctx.send(result)
        else:
            file = open('message.txt', 'w')
            file.write(result)
            file.close
            file = open('message.txt', 'r')
            await ctx.send(file=discord.File(file))
        
@client.command()
async def leavevc(ctx):
    global closingflag
    for x in client.voice_clients:
        if x.guild == ctx.guild:
            closingflag = True
            await x.disconnect()
            break
    
# @client.command()
# async def chess(ctx):
#     global globboard
#     cmc = ctx.message.content.split(' ')[1:]
#     if not ctx.author.voice or not ctx.author.voice.channel:
#         return
#     chan = ctx.author.voice.channel
#     if client.voice_clients:
#         for x in client.voice_clients:
#             if x.guild == ctx.guild:
#                 listen = x
#     else:
#         listen = await chan.connect()
#     users = []
#     pgn = []
#     for x in range(len(cmc)):
#         user = hm.getmember(ctx.guild, cmc[x])
#         if user:
#             users.append(user.id)
#         else:
#             pgn.append(cmc[x])
#     pgn = ' '.join(pgn)
# #     if not globboard:
#     msg = await ctx.channel.send(f'Making board...')
#     globboard = pc.Board(message=msg.id, userturn=users[0], users=users, channel=ctx.channel.id, pgn=pgn)
#     await msg.edit(content=globboard.pgn)
#     if pgn:
#         pgnlist = an.pgntolist(pgn)
#         for x in pgnlist:
#             an.parse(x, globboard, True)
#     
#     imgboard = im.displayboard(globboard, 'W')
#     imgboard.save('chessclasses/state.png', format='PNG')
#     implosion = client.get_user(371801273953026050)
#     imgondiscord = await implosion.send(file=discord.File('chessclasses/state.png'))
#     url = imgondiscord.attachments[0].url
#     embed = discord.Embed(title='Making board...')
#     embed.set_image(url=url)
#     await msg.edit(content=msg.content, embed=embed)
#     '''put the base board here'''
#     def newcon(msg, nothing=None):
#         global closingflag
#         global globboard
#         closingflag = False
#         listen.listen(bs)
#         while(True):
#             recog = sr.Recognizer()
#             if len(bs.bytearr_buf) > 960000:
#                 
#                 idx = bs.bytes_ps * 3
#                 audioslice = bs.bytearr_buf[:idx]
#                 if any(audioslice):
#                     idx_strip = audioslice.index(next(filter(lambda x: x!=0, audioslice)))
#                     if idx_strip:
#                         bs.freshen(idx_strip)
#                         audioslice = bs.bytearr_buf[:idx]
#                     audio = sr.AudioData(bytes(audioslice), bs.sample_rate, bs.sample_width)
#                     try:
#                         voicetext = recog.recognize_wit(audio, 'Q7ZVTDOGVOHEB7SX2CDWKQYW7D4FJJHD')
#                     except sr.UnknownValueError:
#                         print("ERROR: Couldn't understand.")
#                     except sr.RequestError as e:
#                         print(f"ERROR: Could not request results{e}")
#                     if voicetext:
#                         
#                         try:
#                             parsed = an.parse(voicetext, globboard, True)
#                         except: print(voicetext, '- invalid text')
#                         else: print(voicetext)
#                         if parsed:
#                             if parsed[0]:
#                                 imgboard = im.displayboard(globboard, globboard.turn, parsed[3], parsed[4])
#                                 imgboard.save('chessclasses/state.png', format='PNG')
                            # implosion = client.get_user(371801273953026050)
                            # fut = asyncio.run_coroutine_threadsafe(implosion.send(file=discord.File('chessclasses/state.png')), client.loop)
                            # while(not fut.done()):
                            #     asyncio.sleep(.1)
                            # imgondiscord = fut.result()
                            # url = imgondiscord.attachments[0].url
                            # embed = discord.Embed(title=parsed[-1])
                            # embed.set_image(url=url)
#                             if globboard.turn == 'B' and globboard.moves() > 0:
#                                 globboard.pgn += ' ' + str(globboard.moves() + 1) + '.'
#                             globboard.pgn += ' ' + parsed[1]
#                             
#                             asyncio.run_coroutine_threadsafe(msg.edit(content=f'{globboard.pgn}', embed=embed), client.loop)
#                         
#                 bs.freshen(idx)
#                 listen.stop_listening()
#                 
#                 listen.listen(discord.reader.UserFilter(bs, client.get_user(globboard.userturn)))
#             if '#' in msg.content:
#                 asyncio.run_coroutine_threadsafe(msg.edit(content=f'{msg.content}\n{client.get_user(globboard.userturn).name} lost'), client.loop)
#             if closingflag:
#                 print('closing flag')
#                 break
# #         except:
# #             await listen.disconnect()
#     post_thread = Thread(target=newcon, args=(msg, None))
#     post_thread.start()
# #     loop = asyncio.get_event_loop()
# #     pool = futures.ThreadPoolExecutor()
# #     future = await asyncio.shield(loop.run_in_executor(pool, newcon))
# #     await asyncio.wait_for(future, timeout=1)
    
@client.command()
async def append(ctx):
    if str(ctx.author) != "Tiln#0416":
        return
    if await hm.helpredirect(ctx, client): return
    cmc = ctx.message.content.split(' ', 1)[1]
    async for x in ctx.channel.history(limit=100):
        if x.author.id == client.user.id:
            await x.edit(content=x.content+cmc.replace('\\n', '\n'))
            break
    global mes_sageid
    mes_sageid = ctx.message.id
    await ctx.message.delete()
    
@client.command()
async def replace(ctx):
    if str(ctx.author) != "Tiln#0416":
        return
    if await hm.helpredirect(ctx, client): return
    cmc = ctx.message.content.split(' ', 1)[1].replace('\\n', '\n').split('|', 1)
    async for x in ctx.channel.history(limit=100):
        if x.author.id == client.user.id:
            await x.edit(content=x.content.replace(cmc[0], cmc[1]))
            break
    global mes_sageid
    mes_sageid = ctx.message.id
    await ctx.message.delete()
    
@client.command()
async def killbot(ctx):
    if str(ctx.author) == "Tiln#0416":
        global mes_sageid
        mes_sageid = ctx.message.id
        await ctx.message.delete()
        await client.logout()

@client.command()
async def restartbot(ctx):
    if str(ctx.author) == "Tiln#0416" or str(ctx.author) == "AndyVshr#1639":
        global mes_sageid
        mes_sageid = ctx.message.id
        await ctx.message.delete()
        os.execl(sys.executable, sys.executable, '"{}"'.format(*sys.argv))

@client.command()
async def printt(ctx):
    if str(ctx.author) == "Tiln#0416" or str(ctx.author) == "AndyVshr#1639":
        print(ctx.message.content)


async def tmfsm2(ctx, type=0):
    cmc = hm.cmc(ctx)
    seconds = 10
    chan = None
    if len(cmc):
        for x in cmc:
            if not chan:
                chan = hm.getchannel(ctx.guild, x)
                if chan:
                    continue
            seconds = hm.dehumantime(x)[0]
    try: await ctx.message.delete()
    except: ""
    if not hm.authorperm(ctx, 'manage_messages'):
        seconds = 10
    if type == 0:
        if chan:
            await chan.send(f'​\n\n'*666+'\n​', delete_after=seconds)
        else:
            await ctx.send(f'​\n\n'*666+'\n​', delete_after=seconds)
    else:
        if chan:
            await chan.send('​' + '\n'*1998 + '​', delete_after=seconds)
        else:
            await ctx.send('​' + '\n'*1998 + '​', delete_after=seconds)

#The maximally floody spam message
@client.command()
async def tmfsm(ctx):
    await tmfsm2(ctx, type=0)
        
@client.command()
async def tfsm(ctx):
    await tmfsm2(ctx, type=0)

@client.command()
async def spam(ctx):
    global mes_sageid
    if await hm.noperms(ctx, 'manage_messages', server=True):
        mes_sageid = ctx.message.id
        await ctx.message.delete()
        return
    cmc = hm.cmc(ctx)

    repetitions = None
    interval = None
    text = ""
    for x in cmc:
        if hm.integer(x):
            if not repetitions:
                repetitions = int(x)
                continue
            if not interval:
                interval = int(x)
                continue
        text += x + ' '
    
    if not repetitions: repetitions = 1

    mes_sageid = ctx.message.id
    await ctx.message.delete()
    for x in range(repetitions):
        await ctx.send(text.strip())
        await asyncio.sleep(interval or 1)
    

@client.command()
async def aptrentcalc(ctx):
    if ctx.guild.id != 481476691009470474:
        return
    cmc = ctx.message.content.replace(',', '').split(" ")[1:]
    
    Ns = []
    for x in cmc:
        try:
            Ns.append(float(x))
        except:
            await ctx.send(f'{x} in not a valid number')
            return
    if len(Ns) < 3:
        await ctx.send(f'Too few arguments')
        return
    Ns.sort(reverse=True)
    if len(Ns) == 3:
        Ns.append(0.00)
    if Ns[2] != int(Ns[2]):
        temp = Ns[2]
        Ns[2] = Ns[3]
        Ns[3] = temp
    Ns[2] = int(Ns[2])
    '''Total rent, portion that is utility, people, fee(for utility payer)'''
    TC = Ns[0] + Ns[1]
    EPR = math.ceil((TC/Ns[2])*100)/100
    UpR = math.ceil((EPR - Ns[1])*100)/100
    await ctx.send(f'Rent: {Ns[0]}\nUtility: {Ns[1]}\nEach person\'s rent: {EPR}\nUtility payer\'s rent(second payment): {UpR}\n')

@client.command()
async def haiku(ctx):
    pass

file = open("tok.txt", 'r')
client.run(file.readline())
file.close()
#     client.run(sys.argv[1])
