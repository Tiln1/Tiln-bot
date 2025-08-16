'''
Created on May 12, 2018

@author: Tiln
'''

import discord
import asyncio
import random  # @UnusedImport
import base65536
import struct
import re  # @UnusedImport
import itertools
import copy
import json
import sympy
from collections import defaultdict 
from pymongo import MongoClient
from datetime import datetime

mc = MongoClient('localhost', 27017)
tilndb = mc.tiln

servers = None
freedomf = None
prefixf = None

class HelpMethods(object):
    # :a: :b: :information_source: :pisces: :m: :scorpio: :virgo: :capricorn: :o2: :o: :parking: :Aries: :negative_squared_cross_mark: :x: :grey_exclamation: :grey_question:
    # emojdup = ['🅰', '🅱', 'ℹ', '♓', 'Ⓜ', '♏', '♍', '♑', '🅾', '⭕', '🅿', '♈', '❎', '❌', '❕', '❔', '✳', '✖']
    
    # :ab: :cl: :id: :ng: :ok: :vs: :wc: :bangbang: :interrobang: :new: :sos: :cool: :free: :10: 
    emojdoub = ['🆎', '🆑', '🆔', '🆖', '🆗', '🆚', '🚾', '‼', '⁉', '🆕', '🆘', '🆒', '🆓', '🔟']
    texttomorse = {'A':'.-', 'B':'-...', 'C':'-.-.', 'D':'-..', 'E':'.', 'F':'..-.', 'G':'--.', 'H':'....', 'I':'..', 'J':'.---', 'K':'-.-', 'L':'.-..', 'M':'--', 'N':'-.', 'O':'---', 'P':'.--.', 'Q':'--.-', 'R':'.-.', 'S':'...', 'T':'-', 'U':'..-', 'V':'...-', 'W':'.--', 'X':'-..-', 'Y':'-.--', 'Z':'--..', '1':'.----', '2':'..---', '3':'...--', '4':'....-', '5':'.....', '6':'-....', '7':'--...', '8':'---..', '9':'----.', '0':'-----', ', ':'--..--', '.':'.-.-.-', '?':'..--..', '/':'-..-.', '-':'-....-', '(':'-.--.', ')':'-.--.-', '?':'-.-.--', "'":"'"}
    # texttomorsedic = {'A':'.-', 'B':'-...', 'C':'-.-.', 'D':'-..', 'E':'.', 'F':'..-.', 'G':'--.', 'H':'....', 'I':'..', 'J':'.---', 'K':'-.-', 'L':'.-..', 'M':'--', 'N':'-.', 'O':'---', 'P':'.--.', 'Q':'--.-', 'R':'.-.', 'S':'...', 'T':'-', 'U':'..-', 'V':'...-', 'W':'.--', 'X':'-..-', 'Y':'-.--', 'Z':'--..', '1':'.----', '2':'..---', '3':'...--', '4':'....-', '5':'.....', '6':'-....', '7':'--...', '8':'---..', '9':'----.', '0':'-----', ', ':'--..--', '.':'.-.-.-', '?':'..--..', '/':'-..-.', '-':'-....-', '(':'-.--.', ')':'-.--.-'}
    
    
    def cmds(self):
        global servers
        if not servers:
            servers = tilndb.servers.find_one()
        return servers
    
    def updatecmds(self, serversu):
        global servers
        servers = serversu
        tilndb.servers.replace_one({}, servers)
    
    def cmddisabled(self, sid, cmd):
        global servers
        if not servers:
            servers = tilndb.servers.find_one()
        server = servers.get(sid) or []
        for x in server:
            if cmd == x:
                return True
        return False
    
    
    def freedom(self, sid):
        global freedomf
        if not freedomf:
            freedomf = tilndb.freedom.find_one()
        server = freedomf.get(sid) or True
        return server
        
    async def updateroles2(self, rolestoadd, rolestoremove, member):
        roles = member.roles
        for x in rolestoremove:
            if x in roles:
                roles.remove(x)
        for x in rolestoadd:
            if x not in roles:
                roles.append(x)
        await member.edit(roles=roles)

         

    async def updateroles(self, ctx, rolestoadd, rolestoremove, client, allroles, specuser=None):
        updater = discord.utils.get(allroles, name='Updater')
        user = ''
        cmcs = ctx.message.content.split(' ')[1]
        
        respond = True
        if specuser is None:
            if cmcs.isdigit():
                user = ctx.message.server.get_member(cmcs)
            else: user = ctx.message.mentions[0]
        else: 
            user = specuser
            respond = False
        if ctx.message.channel.permissions_for(ctx.message.author).manage_roles or updater in ctx.message.author.roles:
            if ((ctx.message.mentions or cmcs.isdigit()) and len(ctx.message.content.split(' ')) > 2) or respond == False:
                roles = user.roles
                for x in rolestoremove:
                    if x in roles:
                        roles.remove(x)
                for x in rolestoadd:
                    if x not in roles:
                        roles.append(x)
                await user.edit(roles=roles)
                if respond:
                    await ctx.send('Successfully updated role(s)')
                return True
            else: await ctx.send('Please format it as ' + ctx.message.content.split(' ')[0] + ' @username role')
        else: await ctx.send("You don't have permission to use that command or that part of that command :sweat_smile: ")
        return False
    
    # async def createpc(self, ctx, owner, catnid="private channels", voice=False, chin=1):
    #     if inter := ctx.interaction:
    #         cmc = arg.split(" ")
    #     else:
    #         cmc = ctx.message.content.split(" ")[1:]
    #     if not (chan := discord.utils.get(ctx.guild.channels, name=cmc[chin]) or discord.utils.get(ctx.guild.channels, mention=cmc[chin])):
    #         if not (cat := discord.utils.get(ctx.guild.categories, name=catnid)) and catnid.isdigit():
    #             cat = discord.utils.get(ctx.guild.categories, id=int(catnid))
    #         if not cat:
    #             try:
    #                 cat = await ctx.guild.create_category(catnid, reason="Setting up private channels")
    #             except discord.HTTPException as e:
    #                 await ctx.channel.send(str(e).split(':')[-1])
    #                 return
    #         overwrites = cat.overwrites
    #         overwrites.update({ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False), owner:discord.PermissionOverwrite(read_messages=True, manage_messages=True, manage_threads=True, mention_everyone=True, priority_speaker=True, move_members=True)})
    #         for x in ctx.guild.roles:
    #             if x.permissions.manage_channels or (x.permissions.manage_messages and x.permissions.ban_members):
    #                 overwrites.update({x: discord.PermissionOverwrite(read_messages=True)})
    #         try:
    #             if voice:
    #                 chan = await ctx.guild.create_voice_channel(cmc[chin], overwrites=overwrites, category=cat, reason="Owner: " + str(owner) + " by command of: " + str(ctx.author) + ".")
    #             else:
    #                 chan = await ctx.guild.create_text_channel(cmc[chin], overwrites=overwrites, category=cat, reason="Owner: " + str(owner) + " by command of: " + str(ctx.author) + ".")
    #             await ctx.channel.send("Channel created")
    #         except discord.HTTPException as e:
    #             await ctx.channel.send(str(e).split(':')[-1])
    #             return
    #     return chan


    async def createpc(self, ctx, owner, chin, catnid="private channels", voice=False):
        if not (chan := discord.utils.get(ctx.guild.channels, name=chin) or discord.utils.get(ctx.guild.channels, mention=chin)):
            if not (cat := discord.utils.get(ctx.guild.categories, name=catnid)) and catnid.isdigit():
                cat = discord.utils.get(ctx.guild.categories, id=int(catnid))
            if not cat:
                try:
                    cat = await ctx.guild.create_category(catnid, reason="Setting up private channels")
                except discord.HTTPException as e:
                    await ctx.channel.send(str(e).split(':')[-1])
                    return
            overwrites = {ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False), owner:discord.PermissionOverwrite(read_messages=True, manage_messages=True, manage_threads=True, mention_everyone=True, create_polls=True, priority_speaker=True, move_members=True)}
            for x in ctx.guild.roles:
                if x.permissions.manage_channels or (x.permissions.manage_messages and x.permissions.ban_members):
                    overwrites.update({x: discord.PermissionOverwrite(read_messages=True)})
            try:
                if voice:
                    chan = await cat.create_voice_channel(chin, reason="Owner: " + str(owner) + " by command of: " + str(ctx.author) + ".")
                else:
                    chan = await cat.create_text_channel(chin, reason="Owner: " + str(owner) + " by command of: " + str(ctx.author) + ".")
                overwrites2 = chan.overwrites
                overwrites2.update(overwrites)
                synced = chan.permissions_synced
                await chan.edit(overwrites=overwrites2)
                await ctx.channel.send(f"Channel created {chan.mention}\nPermissions synced: {synced}")
            except discord.HTTPException as e:
                error = str(e).split('\n')[-1]
                if 'Missing Permissions' in error:
                    await ctx.channel.send("I don't have permission to do that")
                else:
                    await ctx.channel.send(error)
                return
        return chan
    
    
    def openguildjson(self, fp, gid):
        guilds = eval(f'tilndb.{fp.split("/")[-1].split(".")[0]}.find_one()')
        return guilds.get(gid)
    
            
    def getprefix(self, gid):
        global prefixf
        if not prefixf:
            prefixf = tilndb.prefixes.find_one()
        pf = prefixf.get(str(gid)) or '!?'
        return pf
    
    def setprefix(self, gid, pref):
        global prefixf
        if not prefixf:
            prefixf = tilndb.prefixes.find_one()
        prefixf.update({gid:pref})
        tilndb.prefixes.replace_one({}, prefixf)
    
    
    def wordnumtonum(self, s2, rpldic):
        s = s2.lower()
        for k, v in rpldic:
            s = s.replace(k, v)
        timedict = [('second', 1), ('year', 365.2425*24*3600), ('month', 30.436875*24*3600), ('week', 168*3600), ('day', 24*3600), ('hour', 3600), ('minute', 60)]
        timedict2 = [(x[0], '('+str(x[1])) for x in timedict]
        for k, v in reversed(timedict):
            timedict2.insert(0, (k+'s', '/'+str(v)+')'))
        for k, v in timedict2:
            s = s.replace(k, str(v))
        if s.endswith('+'):
            s = s[:-1]
        openp = len(s) - len(s.replace('(', ''))
        closep = len(s) - len(s.replace(')', ''))
        if openp > closep:
            s = s + ')'*(openp-closep)
        elif closep > openp:
            s = '('*(closep-openp) + s
        inshere = []
        openins = [m.start() for m in re.finditer(r'\(', s)]
        for x in openins:
            if x == 0:
                continue
            if s[x-1] in '0123456789)':
                inshere.append(x-1)
        closeins = [m.start() for m in re.finditer(r'\)', s)]
        for x in closeins:
            if x+1 == len(s):
                continue
            if s[x+1] in '0123456789(qwertyuiopasdfghjklzxcvbnm':
                inshere.append(x+1)
        for x in '0123456789':
            numins = [m.start() for m in re.finditer(x, s)]
            for y in numins:
                if y+1 == len(s):
                    continue
                if s[y+1] in 'qwertyuiopasdfghjklzxcvbnm':
                    inshere.append(y+1)
        #print(traceback.print_exc(file=sys.stdout))
        
        for x in sorted(inshere, reverse=True):
            s = self.insert(s, '*', x)
        return s
    
    def insert (self, sourcestr, insertstr, pos):
        return sourcestr[:pos]+insertstr+sourcestr[pos:]
    
    def humantime(self, seconds, suff=0):
        human = ''
        terms = 0
        suffixes = [['y', 'm', 'd', 'h', 'm', 's', 'ms'], [' years ', ' months ', ' days ', ' hours ', ' minutes ', ' seconds ', ' miliseconds ']]
        if terms < 3 and seconds >= 31104000 and int(seconds//31104000) != 0:
            human += f'{int(seconds//31104000)}{suffixes[suff][0]}'
            terms += 1
        if terms < 3 and seconds >= 2592000 and int(seconds//2592000%12) != 0:
            human += f'{int(seconds//2592000%12)}{suffixes[suff][1]}'
            terms += 1
        if terms < 3 and seconds >= 86400 and int(seconds//86400%30) != 0:
            human += f'{int(seconds//86400%30)}{suffixes[suff][2]}'
            terms += 1
        if terms < 3 and seconds >= 3600 and int(seconds//3600%24) != 0:
            human += f'{int(seconds//3600%24)}{suffixes[suff][3]}'
            terms += 1
        if terms < 3 and seconds >= 60 and int(seconds//60%60) != 0:
            human += f'{int(seconds//60%60)}{suffixes[suff][4]}'
            terms += 1
        if terms < 3 and seconds >= 1 and int(seconds%60) != 0:
            human += f'{int(seconds%60)}{suffixes[suff][5]}'
            terms += 1
        if terms < 3 and seconds >= 0.001 and int(seconds*1000%1000) != 0:
            human += f'{int(seconds*1000%1000)}{suffixes[suff][6]}'
            terms += 1
        return human

    def dehumantime(self, strtoconvert):
        timedict = {'y':365.2425*24*3600, 'o':30.5*24*3600, 'w':7*24*3600, 'd':24*3600, 'h':3600, 'm':60, 's':1}
        timeinseconds = 0
        tim = strtoconvert
        for k, v in timedict.items():
            for x in range(len(tim)):
                if tim[x] == k:
                    timeinseconds += int(tim[:x])*v
                    tim = tim[(x+1):]
                    break
        leftover = tim
        return(timeinseconds, leftover)
    
    def cmc(self, ctx):
        return ctx.message.content.split(' ')[1:]

    def authorperm(self, author, channel, perm):
        if eval(f'channel.permissions_for(author).{perm}'):
            return True
        return False
    
    def meperm(self, channel, perm):
        me = channel.guild.get_member(447268676702437376)
        if eval(f'channel.permissions_for(me).{perm}'):
            return True
        return False
    
    def serverauthorperm(self, author, perm):
        if eval(f'author.guild_permissions.{perm}'):
            return True
        return False
    
    def servermeperm(self, channel, perm):
        me = channel.guild.get_member(447268676702437376)
        if eval(f'me.guild_permissions.{perm}'):
            return True
        return False
    
    
    async def noperms(self, author, channel, *perms, send=True, server=False, annd=True, metoo=True):
        lackingperms = []
        melp = []
        for perm in perms:
            if not server:
                if not self.authorperm(author, channel, perm):
                    lackingperms.append(perm)
                if metoo and not self.meperm(channel, perm) and perm != 'manage_guild':
                    melp.append(perm)
            else:
                if not self.serverauthorperm(author, perm):
                    lackingperms.append(perm)
                if metoo and not self.servermeperm(channel, perm) and perm != 'manage_guild':
                    melp.append(perm)
        tosend = ''
        metosend = ''
        if annd:
            if len(melp) > 0:
                s = ""
                if len(melp) > 1:
                    s = "s"
                strperms = ''
                for x in melp:
                    strperms += x + ', '
                strperms = strperms[:-2]
                metosend = f"\nI require the `{strperms}` permission{s} to execute that command."
            if len(lackingperms) > 0:
                s = ""
                if len(lackingperms) > 1:
                    s = "s"
                strperms = ''
                for x in lackingperms:
                    strperms += x + ', '
                strperms = strperms[:-2]
                tosend = f"You must have the `{strperms}` permission{s} to use that command."
            elif len(melp) < 1:
                return False
            
            if send and (tosend or metosend):
                return await channel.send(tosend+metosend)
            else:
                return tosend
        else:
            strperms = ', '.join(perms)
            if len(melp) == len(perms):
                s = ''
                if len(perms) > 1: s = 's'
                metosend = f"I must have the {strperms} permission{s} to execute that command."
            if len(lackingperms) == len(perms):
                if len(perms) > 1:
                    tosend = f"You must have one of these permissions to use that command: `{strperms}`"
                else:
                    tosend = f"You must have the {strperms} permission to use that command."
            elif len(lackingperms) < len(perms):
                return False
            if send:
                return await channel.send(tosend+metosend)
            else:
                return tosend
    async def noperm(self, ctx, *perms, send=True, server=False, annd=False, metoo=True):
        return (await self.noperms(ctx.author, ctx.channel, *perms, send=send, server=server, annd=annd, metoo=metoo))
        
    async def helpredirect(self, ctx, client):
        if len(ctx.message.content.split(' ')) > 1:
            return False
        pre = self.getprefix(ctx.guild.id)
        ctx.message.content = f'{pre}help {ctx.message.content.replace(pre, "", 1)}'
        await client.process_commands(ctx.message)
        return True
        
    async def enoughmessages(self, ctx, msgs=1, time=1):
        await asyncio.sleep(time)
        messages = await ctx.channel.history(limit=msgs+1).flatten()
        if messages.index(ctx.message) >= msgs:
            return True
        return False
    
    def addprevcalc(self, uid, message):
        users = tilndb.usercalcs.find_one()
        user = users.get(uid) or ('', '')
        return str(user[0]) + message
    
    def getprevvars(self, uid):
        users = tilndb.usercalcs.find_one()
        user = users.get(uid) or ('', {})
        uservars = user[1]
        return {}
    
    def getprevvar(self, uid, var):
        return self.getprevvars(uid).get(var)
        
    def storeprevcalc(self, uid, calc=None, vars=None):  # @ReservedAssignment
        users = tilndb.usercalcs.find_one()
        user = users.get(uid) or (calc if calc != None else '0', {})
        if calc == None:
            calc = user[0]
        uservars = user[1]
        if vars:
            uservars.update(vars)
        users.update({uid: (calc, uservars)})
        tilndb.usercalcs.replace_one({}, users)
        
    def gettarget(self, ctx, posstarget):
        target = None
        if '#' in posstarget:
            strofuser = posstarget.split('#')
            target = discord.utils.get(ctx.guild.members, name=strofuser[0], discriminator=strofuser[1])
        if not target:
            try:
                n = int(posstarget)
                if n > 10000000000000000:
                    target = discord.utils.get(ctx.guild.members, id=n) or discord.utils.get(ctx.guild.roles, id=int(posstarget))
            except: ""
        if posstarget[3:-1].isdigit() and not target:
            n = int(posstarget[3:-1])
            if n > 10000000000000000:
                target = discord.utils.get(ctx.guild.members, id=n)
        if not target:
            target = discord.utils.get(ctx.guild.members, mention=posstarget) or discord.utils.get(ctx.guild.roles, mention=posstarget) or discord.utils.get(ctx.guild.roles, name=posstarget)
        return target
    
    def getchannel(self, guild, posschannel, byname=True):
        posschannel = str(posschannel)
        channel = None
        if posschannel.isdigit():
            n = int(posschannel)
            if n > 10000000000000000:
                channel = guild.get_channel_or_thread(n)
        else:
            both = list(guild.channels)+list(guild.threads)
            channel = discord.utils.get(both, mention=posschannel)
            if not channel and byname:
                channel = discord.utils.get(both, name=posschannel)
        return channel
    
    def getrole(self, guild, possrole, byname=True):
        role = None
        if possrole.isdigit():
            n = int(possrole)
            if n > 10000000000000000:
                role = discord.utils.get(guild.roles, id=int(possrole))
        else:
            role = discord.utils.get(guild.roles, mention=possrole)
            if not role and byname:
                role = discord.utils.get(guild.roles, name=possrole)
        return role
    
    def is_emoji(self, strng):
        emoj = re.compile("["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
            u"\U00002500-\U00002BEF"  # chinese char
            u"\U00002702-\U000027B0"
            u"\U00002702-\U000027B0"
            u"\U000024C2-\U0001F251"
            u"\U0001f926-\U0001f937"
            u"\U00010000-\U0010ffff"
            u"\u2640-\u2642" 
            u"\u2600-\u2B55"
            u"\u200d"
            u"\u23cf"
            u"\u23e9"
            u"\u231a"
            u"\ufe0f"  # dingbats
            u"\u3030"
                        "]+", re.UNICODE)
        return re.match(emoj, strng)

    def getemoji(self, guild, possemoji):
        emoji = None
        if possemoji.isdigit():
            n = int(possemoji)
            if n > 10000000000000000:
                emoji = discord.utils.get(guild.emojis, id=int(possemoji))
        elif ':' in str(possemoji):
            emoji = discord.utils.get(guild.emojis, id=int(possemoji.split(':')[2][:-1]))
        elif self.is_emoji(possemoji):
            emoji = possemoji
        return emoji
    
    def getmember(self, guild, possmember, byname=True):
        member = None
        if '#' in possmember:
            member = discord.utils.get(guild.members, name=possmember.split('#')[0], discriminator=possmember.split('#')[1])
        if possmember.isdigit() and not member:
            n = int(possmember)
            if n > 10000000000000000:
                member = discord.utils.get(guild.members, id=n)
        if possmember[2:-1].isdigit() and not member:
            n = int(possmember[2:-1])
            if n > 10000000000000000:
                member = discord.utils.get(guild.members, id=n)
        if possmember[3:-1].isdigit() and not member:
            n = int(possmember[3:-1])
            if n > 10000000000000000:
                member = discord.utils.get(guild.members, id=n)
        if not member:
            member = discord.utils.get(guild.members, mention=possmember)
        if not member and byname:
            members = [x for x in guild.members if x.nick == possmember]
            if len(members) == 1:
                member = members[0]
        if not member and byname:
            members = [x for x in guild.members if x.name == possmember]
            if len(members) == 1:
                member = members[0]
        return member
    
    def getguild(self, client, possguild):
        possguild = str(possguild)
        guild = None
        if possguild.isdigit():
            guild = client.get_guild(int(possguild))
        if not guild:
            guild = discord.utils.get(client.guilds, name=possguild)
        return guild
    
    def makeRPpoll(self, polloptions, emojis=None):
        emojAN = ['🇦', '🇧', '🇨', '🇩', '🇪', '🇫', '🇬', '🇭', '🇮', '🇯', '🇰', '🇱', '🇲', '🇳', '🇴', '🇵', '🇶', '🇷', '🇸', '🇹', '🇺', '🇻', '🇼', '🇽', '🇾', '🇿', '0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']
        allunique = False
        firstchars = [x.lower()[0] for x in polloptions]
        if len(set(firstchars)) == len(polloptions) and [True]*len(polloptions) == [96 < ord(x) < 123 for x in firstchars]:
            allunique = True
        s = ''
        if emojis:
            for emoji, x in zip(emojis, polloptions):
                s += f'\n{emoji} {x}'
            return(s, emojis)
        else:
            reactions = []
            for idx, x in enumerate(polloptions):
                if allunique:
                    emoji = emojAN[ord(x.lower()[0])-97]
                else:
                    emoji = emojAN[idx]
                s += f'\n{emoji} {x}'
                reactions.append(emoji)
            return (s, reactions)
        
    def rpcollection(self, rankedpairs, trgdic, ctx, btime):
        responses = rankedpairs.get('responses')
        responses2 = copy.deepcopy(responses)
        alloptions = rankedpairs.get('options')
        alloptions2 = copy.deepcopy(alloptions)
        
        trgdic2 = {}
        for x, z in trgdic.items():
            if 'role' in str(type(x)):
                for y in responses.keys():
                    member = ctx.guild.get_member(int(y))
                    if not member: continue
                    if x in member.roles and member not in trgdic.keys():
                        trgdic2.update({y: z})
            else:
                trgdic2.update({x.id: z})
        supertally = []
        placement = 1
        count = 0
        lao2 = len(alloptions)
        while(len(alloptions) > 1):
            count += 1
            if count > lao2:
                print(f"Infiniteloop, alloptions: {alloptions}")
                break
            tally = []
            for x in list(itertools.combinations(alloptions, 2)):
                pairtally = [0, 0]
                for memberid, y in responses.items():
                    member = ctx.guild.get_member(int(memberid))
                    if not member: continue
                    if member.joined_at > btime:
                        continue 
                    mult = trgdic2.get(memberid)
                    if mult == None:
                        mult = 1
                    pos = None
                    if x[0] in y:
                        pos = y.index(x[0])
                    if x[1] in y:
                        pos1 = y.index(x[1])
                        if pos is not None:
                            if pos1 < pos:
                                pairtally[1] += mult
                            else:
                                pairtally[0] += mult
                        else:
                            pairtally[1] += mult
                    elif pos is not None:
                        pairtally[0] += mult
                tally.append([pairtally, x])
            
            #sort, lock, avoid loops
            tally = sorted(tally, key=lambda x: self.ratio(x[0][0], x[0][1]), reverse=True)
            sources = []
            sources2 = defaultdict(list)
            sources3 = defaultdict(list)
            for x in tally:
                if x[0][0] > x[0][1]:
                    source = x[1][0]
                    destination = x[1][1]
                elif x[0][1] > x[0][0]:
                    source = x[1][1]
                    destination = x[1][0]
                else: continue
                sources3[source].append(destination)
                if self.cycle(sources3, destination, destination):
                    sources3 = copy.deepcopy(sources2)
                    continue
                sources2[source].append(destination)
                sources.append(source)
            
            if not sources:
                sources = alloptions
            sourceslist = sorted([[x, sources.count(x)] for x in set(sources)], key=lambda x: x[1], reverse=True)
            
            maximums = [(x[0], placement) for x in sourceslist if x[1] == sourceslist[0][1]]
            supertally += maximums
            placement += len(maximums)
            for y in maximums:
                alloptions.remove(y[0])
                for memberid, vote in responses.items():
                    sett = set(vote).intersection(alloptions)
                    responses.update({memberid: [x for x in vote if x in sett]})
        if len(alloptions):
            supertally.append((alloptions[0], placement))           
        
        optionstable = {}
        baselist = [0]*lao2
        for x in alloptions2:
            optionstable.update({x: copy.copy(baselist)})
        for memberid, y in responses2.items():
            member = ctx.guild.get_member(int(memberid))
            if not member: continue
            if member.joined_at > btime:
                continue
            mult = trgdic2.get(memberid)
            if mult == None:
                mult = 1
            else: mult = int(mult)
            for idz, z in enumerate(y):
                optionstable[z][idz] += mult
        return [supertally, optionstable]
    
    def ratio(self, n1, n2):
        if n1+n2 == 0:
            return 0
        return abs(n1-n2)/(n1+n2)
    def cycle(self, sources, dest, destorig):
        for x in sources[dest]:
            if x == destorig:
                return True
            if self.cycle(sources, x, destorig):
                return True
        return False
    
    def groupedsplit(self, string, splitchar='"', sep=' '):
        tempstr = ''
        splitstr = []
        inquote = False
        for x in string:
            if x in (splitchar+splitchar if splitchar != '"' else '"”“'):
                inquote = not inquote
                continue
            if x == sep and not inquote:
                splitstr.append(tempstr)
                tempstr = ''
                continue
            tempstr += x
        splitstr.append(tempstr)
        return splitstr
    
    def bracesplit(self, string, braces=('{', '}')):
        tempstr = ''
        splitstr = []
        bracedvars = []
        nobrace = []
        inbraces = False
        for x in string:
            entryorexit = True
            if x == braces[0]:
                inbraces = True
            elif x == braces[1]:
                inbraces = False
            else: entryorexit = False
            if x == ' ' and not inbraces:
                if len(tempstr) > 0:
                    splitstr.append(tempstr)
                    nobrace.append(tempstr)
                    tempstr = ''
                continue
            if entryorexit:
                if len(tempstr) > 0:
                    splitstr.append(tempstr)
                    if inbraces:
                        nobrace.append(tempstr)
                    else:
                        bracedvars.append(tempstr)
                    tempstr = ''
                continue
            if x == ' ' and len(tempstr) == 0: continue
            tempstr += x
        if tempstr:
            splitstr.append(tempstr)
            nobrace.append(tempstr)
        return [splitstr, bracedvars, nobrace]
        
    def isdigit(self, n):
        try:
            int(n)
            return True
        except ValueError:
            return False
        
    def texttomorse(self, text):
        words = text.split(' ')
        morse = ""
        for x in words:
            for y in x:
                morse += self.texttomorse[y] + ' '
            morse = morse [:-1]
            morse += '/'
        return morse[:-1]
    
    def morsetotext(self, morse):
        morsetotext = {v: k for k, v in self.texttomorse.items()}
        words = morse.split('  ')
        text = ""
        for x in words:
            letters = x.split(' ')
            for y in letters:
                text += morsetotext[y]
            text += ' '
        return text

    async def countingincrement(self, message, countingf, client):
        #load dictionaries
        gid = str(message.guild.id)
        gc = countingf.get(gid) or {}
        cid = str(message.channel.id)
        chanc = gc.get(cid) or {}
        #store in dictionary
        if chanc and chanc.get('inc') != 'off':
            base = chanc.get('base') or '10'
            cur = chanc.get('current')
            strbaseconv = self.converthelper(cur, '10', str(base))
            intbaseconv = None
            try: intbaseconv = int(strbaseconv)
            except: pass
            inc = chanc.get('inc').replace('^', '**')
            if inc == "dictionary":
                file = open('dictionary.json', 'r+')
                dictionary = json.load(file)
                file.close()
                words = sorted(list(dictionary.keys()))
                if message.content != words[int(cur)]:
                    try:
                        await message.delete()
                    except (discord.Forbidden, discord.NotFound): pass
                    return
            elif message.content != strbaseconv and message.content != '{:,}'.format(intbaseconv):
                try:
                    await message.delete()
                except (discord.Forbidden, discord.NotFound): pass
                return
            
            
            if inc == "1":
                num = len(cur)
            else:
                num = int(cur)
            reactions = []
            reactionables = {"sympy.isprime(num)": ['🇵', '🇷', '🇮', '🇲', '🇪'],
                            "message.content == message.content[::-1]": ['🇵','🇦','🇱','🇮','🇳','🇩','🇷','🇴','🇲','🇪'], 
                            "num == int(num**0.5)**2": self.numtoreactions(int(num**0.5)) + ['🇸', '🇶', '🇺', discord.utils.get(client.emojis, name="a_", id=448623554292875266), '🇷', discord.utils.get(client.emojis, name="e_", id=448623554582282260), discord.utils.get(client.emojis, name="d_", id=448623287782604801)],
                            }
            for k, v in reactionables.items():
                if inc == "dictionary": continue
                if inc == '1' and k == "message.content == message.content[::-1]":
                    continue
                if inc == 'prime' and k != "message.content == message.content[::-1]":
                    continue
                if eval(k.replace('__', '')):
                    if len(reactions):
                        reactions.append('➕')
                    reactions += v
            if len(reactions):
                reactions.append('🎉')
            if inc == 'prime':
                cur = sympy.nextprime(cur)
                chanc.update({'current':str(cur)})
            elif inc == 'dictionary':
                cur = int(cur) + 1
                chanc.update({'current':str(cur)})
            else:
                cur = eval(cur + inc)
                chanc.update({'current':str(cur)})
            gc.update({cid:chanc})
            countingf.update({gid:gc})
            #write to file
            tilndb.counting.replace_one({}, countingf)
            if base != '10' or inc == 'prime':
                await self.countingtopic(str(cur), str(base), message.channel)
            for y in reactions:
                await message.add_reaction(y)

    async def countingtopic(self, num, base, chan):
        await asyncio.sleep(7)

        countingf = tilndb.counting.find_one()
        gid = str(chan.guild.id)
        gc = countingf.get(gid) or {}
        cid = str(chan.id)
        chanc = gc.get(cid) or {}
        cur = chanc.get('current')
        
        if cur != num:
            return
        s = num
        if base != '10':
            strbaseconv = self.converthelper(num, '10', base)
            t = '\_'
            s = f'{strbaseconv.replace("_", t)} || '
            subress = []
            for idx, x in enumerate(strbaseconv):
                exp = (len(strbaseconv) - idx - 1)
                subres = self.converthelper(f'{x}{"0"*exp}', base, 10, skip=False)
                base10x = self.converthelper(f'{x}', base, 10, skip=False)
                if subres == '00':
                    subres = '0'
                if base10x == '00':
                    base10x == '0'
                s += f'({base10x}/{x.replace("_", t)})\*{base}^{exp} = {subres}, '
                subress.append(subres) 
            s += f'{" + ".join(subress)} = {num}'

        try: await chan.edit(topic=s[:2000])
        except: return



    def basedict(self, base):
        basedic = {    
        'allow' : ' abcdefghijklmnopqrstuvwxyz', 'allup' : ' ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'alpha' : ' abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', 'text': ' ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.,',
        '64' : '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_',
        'ascii': '                                 !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~                                  ¡¢£¤¥¦§¨©ª«¬­®¯°±²³´µ¶·¸¹º»¼½¾¿ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿ',
        '65536' : '65536', 'time' : ['00','01','02','03','04','05','06','07','08','09',10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59]
        }
        if self.isdigit(base):
            if int(base) < 64:
                return basedic.get('64')[:int(base)]
        return basedic.get(base)

    def converthelper(self, inp, source, target, skip=False):
        return self.convert(inp, self.basedict(source), self.basedict(target), skip)

    def convert(self, inp, source, target, skip=False):
        if source == target:
            return inp
        if source == '65536':
            source = '0123456789'
            l = len(inp) if len(inp) > 3 else len(inp)+1
            s = '>'
            s += 'Q'*(l//4)
            s += 'L' if l%4 == 3 else 'H' if l%4 == 2 else 'B' if l%4 == 1 else ''
            truct = base65536.decode(inp)
            total = 0
            count = 0 
            for x in struct.unpack(s, truct):
                total += x*(2**64)**count
                count += 1
            inp = str(total)
        if type(source) == list: 
            return "Cannot currently convert from time."
        if type(target) == list and not skip:
            b60str = self.convert(inp, source, target, skip=True)
#             print(b60str)
            b60 = []
            for x in range(0, len(b60str)-1, 2):
                b60.append(b60str[x:x+2][::-1])
            minu = int(b60[-1])
            hour = 0
            counter = 0
            for x in b60[:-1][::-1]:
                hour += int(x)*60**counter
                counter += 1
            hour = hour%24
            return f'{hour}:{"0"*(2-len(str(minu)))}{minu}'           
        
        if target == '65536':
            b10 = int(self.convert(inp, source, '0123456789'))
            nums = []
            s = '>'
            while b10 > 2**64-1:
                s += 'Q'
                nums.append(b10 % 2**64)
                b10 = b10//(2**64)
            if b10 > 2**32-1:
                s += 'Q'
            elif b10 > 2**16-1:
                s += 'L'
            elif b10 > 2**8-1:
                s += 'H'
            else:
                s += 'B'
            nums.append(b10)
            
            return base65536.encode(struct.pack(s, *nums))
        sbase = len(source)
        tbase = len(target)
        if tbase == 1: return False # infinite loop otherwise, below.
        inp = inp[::-1]
        num = 0
        startswith0 = False
        if inp[-1] == source[0]:
            startswith0 = True
        try:
            for x in range(0, len(inp)):
                num += source.index(inp[x])*(sbase**x)
        except: return
        string = ""
        while(num >= 1):
            string += str(target[num % tbase])
            num = num//tbase
        if startswith0:
            string += (target[0])
        return string[::-1]
    
    def cap(self, toCap):
        if ord(toCap[0]) > 96 and ord(toCap[0]) < 123:
            toCap = chr(ord(toCap[0]) - 32) + toCap[1:]
        return toCap
    
    def int_check(self, num):
        try: int(num)
        except: return False
        return int(num)

    def mod(self, n, m):
        return n - n // m * m
    
    def integer(self, num):
        try: int(num)
        except: return False
        return True
    
    def rankednum(self, num):
        if 10 < num and num < 14:
            return str(num) + 'th'
        ranks = ['th', 'st', 'nd', 'rd', 'th', 'th', 'th', 'th', 'th', 'th']
        return str(num) + str(ranks[num%10])
    
    def numtoreactions(self, num):
        return [['0⃣', '1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣'][int(x)] for x in str(num)]
    
    async def fourtwenty(self, client):
        timelist = [(14, 0, 'Kiribati'), (13, 45, 'Chatham Islands'), (13, 0, 'New Zealand'), (12, 0, 'Fiji'), (11, 0, 'Melbourne, Australia'),
                    (10, 30, 'Adelaide, Australia'), (10, 0, 'Brisbane, Australia'), (9, 30, 'Darwin, Australia'), (9, 0, 'Japan'),
                    (8, 45, 'Eucla, Australia'), (8, 0, 'The entirety of China'), (7, 0, 'Thailand'), (6, 30, 'Myanmar'),
                    (6, 0, 'Bangladesh'), (5, 45, 'Nepal'), (5, 30, 'India'), (5, 0, 'Pakistan'),
                    (4, 30, 'Afghanistan'), (4, 0, 'Azerbaijan'), (3, 30, 'Iran'), (3, 0, 'Moscow, Russia'),
                    (2, 0, 'Greece'), (1, 0, 'Germany'), (0, 0, 'United Kingdom'), (-1, 0, 'Praia, Cabo Verde'),
                    (-2, 0, 'Pernambuco, Brazil'), (-3, 0, 'Buenos Aires, Brazil'), (-3, -30, 'Newfoundland, Canada'), (-4, 0, 'Caracas, Venuzuela'), (-5, 0, 'New York'),
                    (-6, 0, 'Illinois'), (-7, 0, 'Colorado'), (-8, 0, 'California'), (-9, 0, 'Alaska'),
                    (-9, -30, 'Taiohae, Marquesas Islands'), (-10, 0, 'Hawaii'), (-11, 0, 'Alofi, Niue'), (-12, 0, 'Baker Island, USA')
                    ]
        while(1 == 1):
            await asyncio.sleep(55)
            d = datetime.utcnow()
            # print(d.year, d.day) # 2020 29
            for hour, minute, name in timelist:
                if ((d.day == 1 and hour <= 0) or (d.day == 31 and hour > 0))and (d.hour+hour)%24 == 0 and (d.minute+minute)%60 == 0:
                    try:
                        await client.get_guild(287817748753678346).get_channel(689053728136888350).send(f'Happy New Year in {name}!')
                    except: pass
                    await asyncio.sleep(600)
    async def dup_char_to_emoji(self, c, dup, emojdup):
#         try:
#             return emojdupdict[c][dup.count('a')]
#         except:
#             return emojdupdict[c][0]
        if c == 'a':
            if c in dup:
                if 'aaa' in ''.join(dup):
                    return emojdup[0]
                elif 'aa' in ''.join(dup):
                    return emojdup[1]
                else:
                    return emojdup[2]
            else: return emojdup[3]
        elif c == 'b':
            if c in dup:
                return emojdup[4]
            else: return emojdup[5]
        elif c == 'c':
            if c in dup:
                return emojdup[6]
            else: return emojdup[7]
        elif c == 'd':
            if c in dup:
                if 'dd' in ''.join(dup):
                    return emojdup[8]
                else:
                    return emojdup[9]
            else: return emojdup[10]
        elif c == 'e':
            if c in dup:
                if 'eee' in ''.join(dup):
                    return emojdup[11]
                elif 'ee' in ''.join(dup):
                    return emojdup[12]
                else:
                    return emojdup[13]
            else: return emojdup[14]
        elif c == 'f':
            if c in dup:
                return emojdup[15]
            else: return emojdup[16]
        elif c == 'g':
            if c in dup:
                return emojdup[17]
            else: return emojdup[18]
        elif c == 'h':
            if c in dup:
                if 'hh' in ''.join(dup):
                    return emojdup[19]
                else:
                    return emojdup[20]
            else: return emojdup[21]
        elif c == 'i':
            if c in dup:
                if 'iii' in ''.join(dup):
                    return emojdup[22]
                elif 'ii' in ''.join(dup):
                    return emojdup[23]
                else:
                    return emojdup[24]
            else: return emojdup[25]
        elif c == 'j':
            return emojdup[26]
        elif c == 'k':
            return emojdup[27]
        elif c == 'l':
            if c in dup:
                if 'll' in ''.join(dup):
                    return emojdup[28]
                else:
                    return emojdup[29]
            else: return emojdup[30]
        elif c == 'm':
            if c in dup:
                if 'mm' in ''.join(dup):
                    return emojdup[31]
                else:
                    return emojdup[32]
            else: return emojdup[33]
        elif c == 'n':
            if c in dup:
                if 'nn' in ''.join(dup):
                    return emojdup[34]
                else:
                    return emojdup[35]
            else: return emojdup[36]
        elif c == 'o':
            if c in dup:
                if 'oo' in ''.join(dup):
                    return emojdup[37]
                else:
                    return emojdup[38]
            else: return emojdup[39]
        elif c == 'p':
            if c in dup:
                return emojdup[40]
            else: return emojdup[41]
        elif c == 'q':
            return emojdup[42]
        elif c == 'r':
            if c in dup:
                if 'rr' in ''.join(dup):
                    return emojdup[43]
                else:
                    return emojdup[44]
            else: return emojdup[45]
        elif c == 's':
            if c in dup:
                if 'ss' in ''.join(dup):
                    return emojdup[46]
                else:
                    return emojdup[47]
            else: return emojdup[48]
        elif c == 't':
            if c in dup:
                if 'ttt' in ''.join(dup):
                    return emojdup[49]
                elif 'tt' in ''.join(dup):
                    return emojdup[50]
                else:
                    return emojdup[51]
            else: return emojdup[52]
        elif c == 'u':
            if c in dup:
                return emojdup[53]
            else: return emojdup[54]
        elif c == 'v':
            if c in dup:
                return emojdup[55]
            else: return emojdup[56]
        elif c == 'w':
            if c in dup:
                return emojdup[57]
            else: return emojdup[58]
        elif c == 'x':
            if c in dup:
                return emojdup[59]
            else: return emojdup[60]
        elif c == 'y':
            if c in dup:
                return emojdup[61]
            else: return emojdup[62]
        elif c == 'z':
            return emojdup[63]
        elif c == '!':
            return emojdup[64]
        elif c == '?':
            return emojdup[65]    
        elif c == '*':
            if c in dup:
                return emojdup[66]
            else: return emojdup[67]
    
    async def doub_char_to_emoji(self, c):
        for idx, x in enumerate(['ab', 'cl', 'id', 'ng', 'ok', 'vs', 'wc', '!!', '!?', 'new', 'sos', 'cool', 'free', '10']):
            if c == x:
                return self.emojdoub[idx]
        
# class BufSink(discord.reader.AudioSink):
#     def __init__(self):
#         self.bytearr_buf = bytearray()
#         self.sample_width = 2
#         self.sample_rate = 96000
#         self.bytes_ps = 192000
# 
#     # just append data to the byte array
#     def write(self, data):
#         self.bytearr_buf += data.data
# 
#     # to prevent the buffer from getting immense, we just cut the part we've
#     # just read from it, using the index calculated when we extracted the part
#     def freshen(self, idx):
#         self.bytearr_buf = self.bytearr_buf[idx:]