'''
Created on Apr 16, 2018

@author: Tiln
'''
import random
import math
import re
from decimal import Decimal
from datetime import datetime
import os.path
import asyncio
import json
import requests
from googlesearch import search
import justext


import platform

import discord
from discord.ext import commands
from discord.ext.commands import Bot

from TilnBot.calceval import NumericStringParser
from TilnBot.otherStuff import HelpMethods

client = Bot(description="General bot", command_prefix="!?", pm_help = False)
client.remove_command('help')

hm = HelpMethods()
asc = ['', '', '', '', '', '', '', '', '    ', '', '', '\n', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ' ', '!', '"', '#', '$', '%', '&', '\'', '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '[', '\\', ']', '^', '_', "`", 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ' ', '¡', '¢', '£', '¤', '¥', '¦', '§', '¨', '©', 'ª', '«', '¬', '­', '®', '¯', '°', '±', '²', '³', '´', 'µ', '¶', '·', '¸', '¹', 'º', '»', '¼', '½', '¾', '¿', 'À', 'Á', 'Â', 'Ã', 'Ä', 'Å', 'Æ', 'Ç', 'È', 'É', 'Ê', 'Ë', 'Ì', 'Í', 'Î', 'Ï', 'Ð', 'Ñ', 'Ò', 'Ó', 'Ô', 'Õ', 'Ö', '×', 'Ø', 'Ù', 'Ú', 'Û', 'Ü', 'Ý', 'Þ', 'ß', 'à', 'á', 'â', 'ã', 'ä', 'å', 'æ', 'ç', 'è', 'é', 'ê', 'ë', 'ì', 'í', 'î', 'ï', 'ð', 'ñ', 'ò', 'ó', 'ô', 'õ', 'ö', '÷', 'ø', 'ù', 'ú', 'û', 'ü', 'ý', 'þ' ]
emojAN = ['🇦', '🇧', '🇨', '🇩', '🇪', '🇫', '🇬', '🇭', '🇮', '🇯', '🇰', '🇱', '🇲', '🇳', '🇴', '🇵', '🇶', '🇷', '🇸', '🇹', '🇺', '🇻', '🇼', '🇽', '🇾', '🇿', '0⃣', '1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣']
#:hash: :exclamation: :question: :heavy_plus_sign: :heavy_minus_sign: :heavy_multiplication_x: :heavy_division_sign: :heavy_dollar_sign:
emojmisc = ['🔥', '❗', '❓', '➕', '➖', '*⃣', '➗', '💲']
emojdoub = ['🆎', '🆑', '🆔', '🆖', '🆗', '🆚', '🚾', '‼', '⁉', '🆕', '🆘', '🆒', '🆓', '🔟']
cmds = (['help', 'superhelp', 'enable', 'disable', 'uroles', 'pin', 'react', 'clearreactions', 'purge', 'collectpoll', 'exclusivizeroles', 'timedroles', 'linkroles', 
        'privatechannels', 'pchan', 'pchancreate', 'pchandelete', 'pchanowned', 'roll', 'rps', 'emojify', 'pfp', 'rolecount', 'calc', 'reminder', 'dtm', 'palindrome', 
        'morse', 'setprefix', 'ping', 'wordcount', 'counting'])
link = 'https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=268774480'



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
    await client.change_presence(activity=discord.Game(name="!?help for help")) #This is buggy, let us know if it doesn't work.
    await hm.autocleanpcdb(client)
    return


@client.event
async def on_message(message):
    rolesset = False
    if message.author.bot:
        return
    if not message.guild:
        for x in message.content.split("\n"):
            mc = x.lower()
            rp = re.compile(r"\d*d(?:\d|\^|\*|-|\+| )+")
            if x.startswith("!?"):
                await client.process_commands(message)
            elif rp.match(x):
                message.content="!?roll "+x
                cmd = message.content.split(" ", 1)[0][2:]
                await client.process_commands(message)
            else:
                mc = mc.replace(",", "")
                nsp = NumericStringParser()
                result = ""
                try:
                    op = "+-*/^%<>"
                    for y in op:
                        if mc.startswith(y):
                            mc = hm.addprevcalc(str(message.author.id), mc)
                            break
                    result = nsp.eval(hm.wordnumtonum(mc, str(message.author.id)))
                    if not str(result) == mc.replace(' ', '') and not str(result) == mc.replace("+", "", 1) and not str(result) == mc.replace("-", "", 1):
                        await message.channel.send(message.channel, str("{:,}".format(result))[:2000])
                        hm.storeprevcalc(str(message.author.id), str(result))
                except: ""
        return
    pre = hm.getprefix(str(message.guild.id))
    if message.content.replace('!', '') == str(client.user.mention):
        await message.channel.send(pre)
    if message.channel == client.get_channel(465333717871886336) and not message.content.startswith("!?emojify") and not message.content.startswith("!?react") and not message.content.startswith("!?purge") and not message.content.startswith("!?calc"):
            message.content = "!?emojify " + message.content.replace("\n", "")
    if message.channel == client.get_channel(465333717871886336) and message.content.startswith("!?calc"):
        nsp = NumericStringParser()
        result = ""
        try: result = nsp.eval(message.content.split(" ", 1)[1])
        except: ""
        if result:
            message.content = "!?emojify " + str(result)
    for x in message.content.split("\n"):
        rp = re.compile(r"\d*d(?:\d|\^|\*|-|\+| )+")
        if x.startswith(pre):
            if not rolesset:
                global roles
                roles = message.guild.roles
            rolesset = True
            
            cmd = x.lower().split(" ", 1)[0][len(pre):]
            for y in range(10, -1, -1):
                x = x.replace(" "*(2**y+1), " ")
            x = x.replace(pre, '!?', 1)
            message.content = x
            if not hm.cmddisabled(str(message.guild.id), cmd):
                await client.process_commands(message)
            else: await message.channel.send("The command \"" + cmd + "\" is disabled in this guild.")
        elif rp.match(x):
            message.content="!?roll "+x
            cmd = message.content.split(" ", 1)[0][2:]
            if not hm.cmddisabled(str(message.guild.id), cmd):
                await client.process_commands(message)
        # ("+" in mc or "-" in mc or "/" in mc or "*" in mc or "^" in mc or "%" in mc or "sin(" in mc or "cos(" in mc or "tan(" in mc or "exp(" in mc or "abs(" in mc or "trunc(" in mc or "round(" in mc or "sqrt(" in mc or "sgn(" in mc or "mod(" in mc or "fact(" in mc) and 
        elif not hm.cmddisabled(str(message.guild.id), "calc") and not message.channel.name == "role-submissions" and not message.channel.name == "general":
            x = x.replace(",", "")
            nsp = NumericStringParser()
            result = ""
            op = "+-*/^%<>"
            for y in op:
                if x.startswith(y):
                    x = hm.addprevcalc(str(message.author.id), x)
                    break
            try:
                result = nsp.eval(hm.wordnumtonum(x, str(message.author.id)))
            except: ""
            else:
                if not str(result) == x.replace(' ', '') and not str(result) == x.replace("+", "", 1) and not str(result) == x.replace("-", "", 1):
                    try:
                        await message.channel.send(str("{:,}".format(result))[:2000])
                    except:
                        print(message.channel.name)
                    hm.storeprevcalc(str(message.author.id), str(result))
    file = open('counting.json', 'r+')
    c = json.load(file)
    file.close()
    #load dictionary
    gid = str(message.guild.id)
    gc = c.get(gid) or {}
    cid = str(message.channel.id)
    cc = gc.get(cid) or {}
    #store in dictionary
    if cc and cc.get('inc') != 'off':
        cur = cc.get('current')
        if message.content != cur:
            try:
                await message.delete()
            except: ""
            return
        inc = cc.get('inc').replace('^', '**')
        cc.update({'current':str(eval(cur + inc))})
        gc.update({cid:cc})
        c.update({gid:gc})
        #write to file
        file = open('counting.json', 'w+')
        file.write(json.dumps(c))
        file.close()
                
        
            
            
@client.event
async def on_member_update(before, after):
    if before.roles == after.roles:
        return
    sid = after.guild.id
    
    file = open('exclusiveroles.json', 'r+')
    exguilds = json.load(file)
    exrg = exguilds.get(sid)
    
    file = open('linkedroles.json', 'r+')
    linkguilds = json.load(file)
    linkrp = linkguilds.get(sid)
    #role added
    for x in after.roles:
        if linkrp:
            for y in linkrp:
                if x.name == y.split(':')[0] and not x in before.roles:
                    await after.add_roles(discord.utils.get(after.guild.roles, name=y.split(":")[1]))
        if exrg:
            for y in exrg:
                if x.name in y.split(':') and not x in before.roles:
                    rtr = []
                    for z in y.split(':'):
                        if not z == x.name:
                            rtr.append(discord.utils.get(after.guild.roles, name=z))
                    await after.remove_roles(rtr)
                    return
                    
    #role removed
    for x in before.roles:
        if linkrp:
            for y in linkrp:
                if x.name == y.split(':')[0] and not x in after.roles:
                    await after.remove_roles(discord.utils.get(after.guild.roles, name=y.split(":")[1]))
                    return



@client.command()
async def ping(ctx):
    if str(ctx.author) == "Tiln#0416":
        toignore = ['Home', 'Games', 'Streams', 'Forums', 'More', 'Home', 'Games', 'Streams', 'Forums', 'Races SpeedRunsLive', 'Resources', 'Podcasts', 'Users', 'About', 'Statistics', 'Changelog', 'API', 'Promotion', 'Help / Contact', 'Donate', 'Patreon', 'Social', 'Twitter', 'Facebook', 'Discord', 'Log in', 'Sign up', 'Log in', 'Username:', 'Password:', 'Forgot passwordCancel', 'Sign up', 'Username', 'E-mail:', 'Confirm e-mail:', 'Cancel', 'Languages (Beta)', 'Hi!', "Because you're a donator, you can have early access to our in-progress language system. There's still a lot for us to do, but we thought you might want to try it out!", 'For more info, check out this thread.', 'Close', 'Advertisement (Log in to hide)']
        
        async for x in ctx.channel.history(limit=None):
            rp = re.compile(r"((?:https?:\/\/)?(?:www\.)?[A-Za-z0-9]{1,}\.(?:(?:com)|(?:net)|(?:org)|(?:tv))[A-Z|a-z|-|_|=|?|0-9|\/]{1,})")
            m = re.findall(rp, x.content)
            for y in m:
                if 'speedrun' in y:
                    response = search(y)
                    s = ""
                    for z in response:
                        s += "<" + z + ">\n"
                        resp = requests.get(z)
                        paragraphs = justext.justext(resp.content, justext.get_stoplist("English"))
                        for w in paragraphs:
                            backup = True
                            if not w.text in toignore:
                                print(w.text)
                                backup = False
                                break
                        if backup:
                            print(y)
                        break
                else: print(y)
    
#         msg = await ctx.channel.get_message(int(ctx.message.content.split(" ")[1]))
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
    pre = hm.getprefix(str(ctx.guild.id))
    base = False
    if len(com)>1:
        c = com[1]
        if not hm.cmddisabled(str(ctx.guild.id), c):
            helpdict = ({"disable": "```"+pre+"disable *commandstodisable\n"+pre+"disable role1 role2 role3```",
                "enable": "```"+pre+"enable *commandstoenable\n"+pre+"enable all```",
                "uroles": "```"+pre+""+c+" @member *rolestoadd|*rolestoremove\nExample: "+pre+""+c+" @Tiln Farmer_III Kilofarmer_III Megafarmer_III Gigafarmer_III|Gigafarmer_II Eggs```",
                "pin": "```"+pre+""+c+" @member *rolestoadd|*rolestoremove\nExample: "+pre+""+c+" @Tiln Farmer_III Kilofarmer_III Megafarmer_III Gigafarmer_III|Gigafarmer_II Eggs```",
                "clearreactions": "```"+pre+""+c+" <@member/messageid/number of messages>\n<> Means optional\n```",
                "roll": "```"+pre+""+c+" <<number of dice>d[how large of a dice][plus or minus some number to add to each roll]> <something to do to the total>\nExample: "+pre+""+c+" 5d6+1 +1```",
                "rps": "```"+pre+""+c+" [Rock/Paper/Scissors]```",
                "purge": "```"+pre+""+c+" [number of messages]\nor for deleting a single user's messsages:\n"+pre+""+c+" [@member/userid] [number of messages]\nor for deleting messages except by a certain user:\n"+pre+""+c+" [@member/userid]! [number of messages]```",
                "collectpoll": "```"+pre+""+c+" channelid [number of messages that consist of the poll]```",
                "reminder": "```"+pre+""+c+" *[time][y/o/w/d/h/m/s] Reason for timer\n"+pre+""+c+" 1y It has been a year haha!```",
                "exclusivizeroles": "```"+pre+""+c+" *roles\n"+pre+""+c+" Chicks_and_Chickens Eggs```",
                "timedroles": "```"+pre+""+c+" [time][y/o/w/d/h/m/s] role_name\n"+pre+""+c+" 1y the_best_role```",
                "linkroles": "```"+pre+""+c+" independantrole semi-dependantrole\n"+pre+""+c+" squares rectangles_and_squares```",
                "privatechannels": "```"+pre+""+c+" [enable or disable or [maximum amount of free creation channels] or category(by id or name) or role(by mention, name, or id)]\nor "+pre+""+c+" [owner(by mention, full name, or id)] [channel(by id, name, or mention)] <category(by id or name)>\n<> means optional.```",
                "pchan": "```"+pre+""+c+" [invite or kick or setspectator or setlistener or transferownership] target(role or member(by id, mention or (full)name)) channel(by id, mention, or name)\n```",
                "pchancreate": "```"+pre+""+c+" channelname <category(by name or id)> <thing here if you want voice instead>\n```",
                "pchandelete": "```"+pre+""+c+" channel(by id, mention or name)\n```",
                "pchanowned": "```"+pre+""+c+"\n```",
                "emojify": "```"+pre+""+c+" [message]```",
                "pfp": "```"+pre+""+c+"<mention>```",
                "rolecount": "```"+pre+"rolecount *roles```",
                "dtm": "```"+pre+"dtm messageid <channelid or channelmention>(if outside sent channel)```",
                "misc": "```"+pre+"roll rolls some dice\n"+pre+"rps plays rock paper scissors\n"+pre+"emojify emojifies a message\n"+pre+"pfp returns your profile picture\n"+pre+"calc returns the calculation results\n"+pre+"dtm generates a url for a message\n```",
                "calc": "```"+pre+"calc expression```",
                "emojify": "```"+pre+"emojify message```",
                "palindrome": "```"+pre+"palindrome message```",
                "morse": "```"+pre+"morse message or morse text```",
                "wordcount": "```"+pre+"wordcount target(by id, mention or name+discriminator)```"
                })
            
            if c == "react":
                if len(com) > 2:
                    b = com[2]
                    if b == "repeats":
                        await ctx.channel.send("```diff\n3 on all letters;\n-j,k,q,z\n+a, a, d, e, e, h, i, i, l, m, n, o, r, s, t, t, !, ?, *, *```")
                        return
                    elif b == "doubles":
                        await ctx.channel.send("```ab, cl, id, ng, ok, vs, wc, !!, "+pre+", new, sos, cool, free, 10```")
                        return
                    elif b == "misc":
                        await ctx.channel.send("```+, -, *, /, $, !, ?```")
                    return
                await ctx.channel.send("```"+pre+""+c+" <@member/messageid> *reactions\n<> Means optional and skippable```")
            await ctx.channel.send(helpdict.get(c) or ""+pre+""+c+" is not currently a command")
        else: await ctx.channel.send(""+pre+""+c+" is disabled")
    else: base = True
    s = ""
    if base:
        s += "```"+pre+"help Displays this command\n"+pre+"help misc for misc commands\n"+pre+"collectpoll collects a poll\n"+pre+"rolecount counts the number of people in the specified role(s)\n"+pre+"pchan "+pre+"pchancreate "+pre+"pchandelete "+pre+"pchanowned Does private channels things\n"
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
async def superhelp(ctx):
    cmc = ctx.message.content.lower().split(" ")[1:]
    pre = '!?'
    if ctx.guild:
        pre = hm.getprefix(str(ctx.guild.id))
    
    shd = ({'basehelp': pre+"superhelp [command] for superhelp on that command. ` ` is the default args separator. Here's a full list of commands:```",
          'superhelp': 'Superhelp: you are currently using the superhelp command. '+pre+'superhelp [command] for superhelp on that command. " " is the default args separator. ',  
          'disable': 'Disable disables commands. Simply specify the commands as arg(s) to disable them. "all" can also be disabled. Commands are enabled by default. Requires the manage server permission.',
          'enable': 'Enable enable commands. Simply specify the commands as arg(s) to enable them. "all" can also be enabled. Commands are enabled by default. Requires the manage server permission.',
          'help': 'Help gives a more simplistic help on commands, non-wordy syntax and short descriptions. Input the commandname as arg1 for help on that command.',
          'uroles': 'Uroles means "update roles". It allows a user to add and/or remove roles through a command. Specify roles to add and remove as args. The "|" character separates roles to add and roles to remove. Removed roles come after. Requires the manage roles permissions or  a role named "Updater"',
          'pin': 'Pin pins a message, either the latest message, a message specified by id, or a user by mention (arg1).',
          'ping': 'Ping returns a (usually) inaccurate round trip time from you to the bot in milliseconds.',
          'react': 'React reacts to a message. Emoji, letters, and numbers are all specifiable. The message can be specified by message id or by mentioning the user you want to react to as arg1. Otherwise/where applicable, reacts to the latest message.',
          'clearreactions': 'Clearreactions clears the reactions off a message. The message can be specified by message id or by mentioning the user you want to react to as arg1. Otherwise/where applicable, clears from the latest message with reactions. Requires the manage messages permission.',
          'purge': 'Purge purges a number of messages specified by a number as arg1 or arg2. arg1 can instead be a user by mention or id or a "!" can be put in front of the id or mention so that the purge only targets messages by other users. Does not purge pinned messages. Requires the manage messages permission.',
          'collectpoll': 'Collectpoll collects a poll from a specified channel. If a poll consists of multiple messages, or you want to collect multiple polls at the same time, a number may be specified. Channelid as arg1 and the number of messages as arg2(if applicable, default 1).',
          'reminder': 'Reminder reminds the command sender after a certain amount of time specified in arg1(exam: 32d4h50s) with an optional reason specified in arg2+.',
          'exclusivizeroles': 'Exclusivizeroles takes a list of roles("_" in place of spaces in role names) in all the args and makes it so that users can only have one role out of the list at any given time unless their highest role is above my highest role. Requires the manage roles permission.',
          'timedroles': 'Timedroles assigns the specified roles(by name("_" in place of spaces)) as args2+ to everyone that has been in the guild for at least the specified time. Time in arg1(exam: 500s). Requires the manage roles permission.',
          'linkroles': 'Linkroles links two roles together. arg1 as the independant role, arg2 as the semi-dependant role, meaning if role1 is added or removed then role2 is added or removed. "_" in place of space for role names. Requires the manage roles permission.',
          '''''''''''''privatechannels': 'Privatechannels . Requires the manage guild and manage channels permissions.',
          'pchan': 'Pchan allows you to manage the members and roles of channels you own. invite, kick, superkick, setspectator, or setlistener as arg1. The intended target(role or member(by id, mention or (full)name)) as arg2. And the intended channel(by id, mention, or name) as arg3(unless you\'re in the target channel).',
          'pchancreate': 'Pchancreate allows a user to create a pchan, with name as arg1, desired category in arg2 and any argument in arg3 to set it as voice. [space] is the "space" within an arg.',
          'pchanowned': 'Pchanowned returns the channels you own in that guild.',
          
           
          })
    s = ""
    if not cmc:
        s = shd.get('basehelp')
        for x in cmds:
            s += x + ','
        s = s[:-1] + "```"
        await ctx.channel.send(s)
    for x in cmc:
        s += "```" if len(cmc) > 1 else ""
        s += shd.get(x) or x + " is not a command as far as I am aware."
        s += "``` " if len(cmc) > 1 else ""
    await ctx.channel.send(s[:2000])
    

@client.command()
async def disable(ctx):
    if ctx.channel.permissions_for(ctx.author).manage_guild:
        file = open('servers.json', 'r+')
        servers = json.load(file)
        sid = str(ctx.guild.id)
        server = servers.get(sid) or []
        
        cmc = ctx.message.content.split(" ")[1:]
        if len(cmc) > 0:
            for x in cmc:
                if x in cmds:
                    disableable = True
                    for y in server:
                        if y == x:
                            disableable = False
                            break
                    if disableable:
                        server.append(x)
                elif x == "all":
                    for y in cmds:
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
        file = open('servers.json', 'w+')
        file.write(json.dumps(servers))
        await ctx.channel.send("Success")
    else: await ctx.channel.send("You don't have permission to use that command :sweat_smile: ")
    

@client.command()
async def enable(ctx):
    if ctx.channel.permissions_for(ctx.author).manage_guild:
        file = open('servers.json', 'r+')
        servers = json.load(file)
        sid = str(ctx.guild.id)
        server = servers.get(sid)
        if not server: return
        cmc = ctx.message.content.split(" ")[1:]
        if len(cmc) > 0:
            for x in cmc:
                if x in cmds:
                    server.remove(x)
                elif x == "all":
                    for y in cmds:
                        server.remove(y)
                    break
        else: return
        servers.update({sid:server})
        file = open('servers.json', 'w+')
        file.write(json.dumps(servers))
        await ctx.channel.send("Success")
    else: await ctx.channel.send("You don't have permission to use that command :sweat_smile: ")
    

@client.command()
async def uroles(ctx):
    rta = []
    rtr = []
    ar = ctx.message.content.split("|")
    add = ar[0].split(" ")
    for x in range(len(add) - 2):                                                               
        rta.append(discord.utils.get(roles, name=add[x+2].replace("_", " ")))
    if len(ar) > 1:
        rem = ar[1].split(" ")
        for x in range(len(rem)):
            rtr.append(discord.utils.get(roles, name=rem[x].replace("_", " ")))
    await hm.updateroles(ctx, rta, rtr, client, roles)
            
            
@client.command()
async def pin(ctx):
    if ctx.channel.permissions_for(ctx.author).manage_messages:
        pinned = False;
        if len(ctx.message.content.split(" ")) > 1:
            mid = ctx.message.content.split(" ")[1]
            if hm.isdigit(mid):
                if int(mid) > 10000:
                    await client.pin_message(await ctx.channel.get_message(mid))
                    await ctx.message.delete()
                    return
        async for x in ctx.channel.history():
            if ctx.message.mentions:
                if not x.content.startswith("!?pin") and x.author == ctx.message.mentions[0]:
                    await client.pin_message(x)
                    pinned = True
                    break
            else:   
                if not x.content.startswith("!?pin"):
                    await client.pin_message(x)
                    pinned = True
                    break
        if not pinned: await ctx.channel.send("The user you are trying to pin is not recent enough or does not exist.")
    else: await ctx.channel.send("You don't have permission to use that command :sweat_smile: ")
    await ctx.message.delete()


@client.command()
async def react(ctx):
    if ctx.channel.permissions_for(ctx.author).add_reactions:
        emojdup = [discord.utils.get(client.emojis, name="a_", id=448623901027860500), discord.utils.get(client.emojis, name="a_", id=485644541567959040), discord.utils.get(client.emojis, name="a_", id=448623554292875266), u'🅰', discord.utils.get(client.emojis, name="b_", id=448623288177000448), u'🅱', discord.utils.get(client.emojis, name="c_", id=448623288185257994), discord.utils.get(client.emojis, name="c_", id=448623554582282240), discord.utils.get(client.emojis, name="d_", id=448623287782604801), discord.utils.get(client.emojis, name="d_", id=448623900834922500), discord.utils.get(client.emojis, name="d_", id=448623554611773440), discord.utils.get(client.emojis, name="e_", id=448623554582282260), discord.utils.get(client.emojis, name="e_", id=448623980753190913), discord.utils.get(client.emojis, name="e_", id=448623288445435914), discord.utils.get(client.emojis, name="e_", id=448623900889186317), discord.utils.get(client.emojis, name="f_", id=448623288189714442), discord.utils.get(client.emojis, name="f_", id=448623554582544384), discord.utils.get(client.emojis, name="g_", id=448623554615836673), discord.utils.get(client.emojis, name="g_", id=448623288109891585), discord.utils.get(client.emojis, name="h_", id=448623554544664586), discord.utils.get(client.emojis, name="h_", id=448623288214880296), u'♓', discord.utils.get(client.emojis, name="i_", id=448623901040443392), discord.utils.get(client.emojis, name="i_", id=448623288277532692), discord.utils.get(client.emojis, name="i_", id=448623554611642368), u'ℹ', discord.utils.get(client.emojis, name="j_", id=448623287833198603), discord.utils.get(client.emojis, name="k_", id=448623288193646609), discord.utils.get(client.emojis, name="l_", id=448623901040443402), discord.utils.get(client.emojis, name="l_", id=448623554670362625), discord.utils.get(client.emojis, name="l_", id=448623288210686003), u'Ⓜ', u'♏', u'♍', discord.utils.get(client.emojis, name="n_", id=448623554628419584), discord.utils.get(client.emojis, name="n_", id=448623288197840926), u'♑', discord.utils.get(client.emojis, name="o_", id=448623288487247882), u'🅾', u'⭕', discord.utils.get(client.emojis, name="p_", id=448623288466276382), u'🅿', discord.utils.get(client.emojis, name="q_", id=448623288281726996), discord.utils.get(client.emojis, name="r_", id=448625035985420289), discord.utils.get(client.emojis, name="r_", id=448623287929667596), discord.utils.get(client.emojis, name="r_", id=448623900771745793), discord.utils.get(client.emojis, name="s_", id=448623554590932992), discord.utils.get(client.emojis, name="s_", id=448623288210554880), discord.utils.get(client.emojis, name="s_", id=448623901044375552), discord.utils.get(client.emojis, name="t_", id=448623287866490881), discord.utils.get(client.emojis, name="t_", id=448623901220536331), discord.utils.get(client.emojis, name="t_", id=448623980849659926), discord.utils.get(client.emojis, name="t_", id=448623554498527233), discord.utils.get(client.emojis, name="u_", id=448623554590933002), discord.utils.get(client.emojis, name="u_", id=448623288470601738), discord.utils.get(client.emojis, name="v_", id=448623288055496725), u'♈', discord.utils.get(client.emojis, name="w_", id=448623288214749187), discord.utils.get(client.emojis, name="w_", id=448623554519629825), '❎', '❌', discord.utils.get(client.emojis, name="y_", id=448623554636808193), discord.utils.get(client.emojis, name="y_", id=448623288210554900), discord.utils.get(client.emojis, name="z_", id=448623288512675840), u'❕', u'❔', u'✳', u'✖']
        doub = ["ab", "cl", "id", "ng", "ok", "vs", "wc", "!!", "!?", "new", "sos", "cool", "free"]
        dup = ["a", "a", "a", "a", "b", "b", "c", "c", "d", "d", "d", "e", "e", "e", "e", "f", "f", "g", "g", "h", "h", "h", "i", "i", "i", "i", "j", "k", "l", "l", "l", "m", "m", "m", "n", "n", "n", "o", "o", "o", "p", "p", "q", "r", "r", "r", "s", "s", "s", "t", "t", "t", "t", "u", "u", "v", "v", "w", "w", "x", "x", "y", "y", "z", "!", "?", "*", "*"]
        #dup = ["a", "b", "i", 'h', "m", "m", "m", "n", "o", "o", "p", "v", "x", "x", "!", "?", "*", "*"]
        duptrans = []
        com = ctx.message.content.split(" ")
        num = 1
        ment = False
        mid = False
        mem = ""
        if hm.isdigit(com[1]):
            if int(com[1]) > 1000000000:
                num = 2
                mid = True
        elif ctx.message.mentions:
            num = 2
            ment = True
            mem = ctx.message.mentions[0]
        async for x in ctx.channel.history():
            if mid:
                x = await ctx.channel.get_message(com[1])
            if (not x.content.startswith("!?react") and (not ment or x.author == mem)) or mid:
                emoji = []
                try:
                    await ctx.message.delete()
                except: ""
                npstr = ctx.message.content.split(" ", num)[num]
                for y in doub:
                    if y in npstr.lower():
                        doubemo = await hm.doub_char_to_emoji(y)
                        npstr = npstr.replace(y, doubemo, 1)
                com = npstr.split(" ")
                for y in range(len(com)):
                    mes = ""
                    if com[y][0] == "<" and com[y][-1] == ">":
                        mes = discord.utils.get(client.emojis, name=com[y].strip("<>").split(":")[1], id=com[y].strip("<>").split(":")[2])
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
                for y in emoji:
                    await x.add_reaction(y)
                return
        await ctx.channel.send("The user you are trying to react to is not recent enough or does not exist.")
        await ctx.message.delete()
    else: await ctx.channel.send("You don't have permission to use that command :sweat_smile: ")
    
    
@client.command()
async def clearreactions(ctx):
    if ctx.channel.permissions_for(ctx.author).manage_messages:
        com = ctx.message.content.split(" ")
        mid = ""
        mem = ""
        if len(com) > 1:
            mid = com[1]
        if hm.isdigit(mid):
            if int(mid) > 10000:
                await ctx.channel.get_message(mid).clear_reactions()
                await ctx.message.delete()
                return
            else:
                mid = int(mid)
        elif ctx.message.mentions:
            mem = ctx.message.mentions[0]
        else: mid = 0
        num = 0
        async for x in ctx.channel.history():
            if not x.content == "!?clearreactions" and x.reactions and (x.author == mem or not mem):
                num += 1
                await x.clear_reactions()
                if num >= mid or not mid:
                    break
    else: await ctx.channel.send("You don't have permission to use that command :sweat_smile: ")
    await ctx.message.delete()
    

@client.command()
async def purge(ctx):
    if ctx.channel.permissions_for(ctx.author).manage_messages:
        cmc = ctx.message.content.split(" ");
        isufi = False
        uid = 0
        abtu = False
        if cmc[1].startswith("!"):
            cmc[1] = cmc[1].replace("!", "", 1)
            abtu = True
        elif cmc[1].endswith("!"):
            cmc[1] = ''.join(cmc[1].rsplit("!", 1))
            abtu = True
        if hm.isdigit(cmc[1]):
            if int(cmc[1]) > 100000:
                isufi = True
                uid = cmc[1]
        if ctx.message.mentions or isufi:
            arg2 = ""
            if len(cmc) > 2:
                arg2 = cmc[2]
            else: arg2 = "99"
            limit = 100
            if hm.isdigit(arg2):
                limit = int(arg2) + 1
            if isufi:
                if not ctx.author == ctx.guild.get_member(uid):
                    await ctx.message.delete()
                    limit -= 1
            else:
                if not ctx.author == ctx.message.mentions[0]:
                    await ctx.message.delete()
                    limit -= 1
        elif hm.isdigit(cmc[1]):
            limit = int(cmc[1]) + 1
        else:
            await ctx.channel.send("No number of messages nor user specified")
            return
        prevlimit = -552
        while limit > 0:
            num = 0
            mess = []
            async for x in ctx.channel.history():
                t = (datetime.utcnow() - x.created_at).total_seconds()
                if t < 1200000 and not x.pinned:
                    if isufi:
                        if x.author == ctx.guild.get_member(uid) and not abtu:
                            mess.append(x)
                            num += 1
                            if num >= limit:
                                break
                        elif not x.author == ctx.guild.get_member(uid) and abtu:
                            mess.append(x)
                            num += 1
                            if num >= limit:
                                break
                    elif ctx.message.mentions:
                        if x.author == ctx.message.mentions[0] and not abtu:
                            mess.append(x)
                            num += 1
                            if num >= limit:
                                break
                        elif not x.author == ctx.message.mentions[0] and abtu:
                            mess.append(x)
                            num += 1
                            if num >= limit:
                                break
                    else:
                        mess.append(x)
                        num += 1
                        if num >= limit:
                            break
                elif not x.pinned:
                    await x.delete()
                    num += 1
                    if num >= 1000 or num >= limit:
                        limit = 0
                        break
            if len(mess) > 1:
                await ctx.channel.delete_messages(mess)
            elif len(mess) == 1:
                await x.delete()
            limit -= num
            if prevlimit == limit: break
            prevlimit = limit
    else: await ctx.channel.send("You don't have permission to use that command :sweat_smile: ")
    

@client.command()
async def collectpoll(ctx):
    cmc = ctx.message.content.split(" ")[1:]
    
    channel = None
    trgdic = {}
    num = None
    before = None
    for x in range(len(cmc)):
        if cmc[x].lower() == 'before':
            if hm.isdigit(cmc[x+1]):
                n = int(cmc[x+1])
                if n > 10000000000000000:
                    before = (channel or ctx.channel).get_message(n)
                    x += 1
                    continue
        if not channel:
            channel = hm.getchannel(ctx, cmc[x])
            if channel:
                continue
            
        target = await hm.gettarget(ctx, cmc[x])
        if target:
            for y in range(x, len(cmc)):
                if hm.isdigit(cmc[y]):  
                    trgdic.update({target:float(cmc[y])})
                    break
            if not trgdic.get(target):
                await ctx.channel.send("You have failed to provide a valid role or user multiplier.")
                return
            continue
        
        if not num and hm.isdigit(cmc[x]):
            n = int(cmc[x])
            if n < 10000000000000000:
                num = n
                continue
    if not channel:
        channel = ctx.channel         
    if not num:
        num = 1
    btime = before.created_at if before else datetime.utcnow()
        
    i = 0
    dic = {}
    async for x in channel.history():
        s = x.content
        if x.reactions:
            i += 1
            mes = x.content.split("\n")
            for y in x.reactions:
                ec = -1
                async for z in y.users():
                    mult = trgdic.get(z)
                    if not mult and z in ctx.guild.members:
                        if z.joinedat < btime:
                            for w in z.roles:
                                mult = trgdic.get(w)
                                if mult:
                                    break
                    if not mult:
                        mult = 1
                    ec += mult
                if int(ec) == ec:
                    ec = int(ec)
                for z in mes:
                    if str(y.emoji) in z:
                        dic.update({z: ec})
                        break
                    s += "\n" + str(y.emoji) + ": " + str(ec)
            await ctx.channel.send(s)
            if i >= num:
                break
    if dic:
        with open('poll.csv', 'w') as file:
            for k in sorted(dic, key=dic.get, reverse=True):
                #s += k + ": " + str(dic[k]) + "\n"
                file.write(str(k.replace(",", "").encode("utf-8")) + "," + str(dic[k]) + "\n")
        file = discord.File('poll.csv')
        await ctx.channel.send(file=file)


@client.command()
async def reminder(ctx):
    cmc = ctx.message.content.split(" ", 2)[1:]
    num = 0
    timedict = {'y':365.2425*24*3600, 'o':30.5*24*3600, 'w':7*24*3600, 'd':24*3600, 'h':3600, 'm':60, 's':1}
    tim = cmc[0]
    for k, v in timedict.items():
        for x in range(len(tim)):
            if tim[x] == k:
                num += float(tim[:x])*v
                tim = tim[(x+1):]
                break
    if len(tim) > 0:
        num += float(tim)
    
    auth = ctx.author.mention
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


@client.command()
async def exclusivizeroles(ctx):
    if ctx.channel.permissions_for(ctx.author).manage_roles:
        cmcs = ctx.message.content.split(" ")[1:]
        exroles = []
        strexroles = []
        for x in cmcs:
            r = discord.utils.get(ctx.guild.roles, name=x.replace("_", " "))
            if not r:
                await ctx.channel.send(x + " is not recognized as a valid role.")
                return
            else: exroles.append(r)
            strexroles.append(x.replace("_", " "))

        file = open('exclusiveroles.json', 'r+')
        guilds = json.load(file)
        sid = str(ctx.guild.id)
        guild = guilds.get(sid) or []
        s = ""
        add = True
        for x in guild:
            if strexroles == x.split(":"):
                add = False
                guild = guild.replace("," + x, "")
        if add:
            for x in strexroles:
                s += x + ":"
            s = s[:-1]
        guild.append(s)
        guilds.update({sid:guild})
        file = open('exclusiveroles.json', 'w+')
        file.write(json.dumps(guilds))
    else: await ctx.channel.send("You don't have permission to use that command :sweat_smile: ")

        
@client.command()
async def timedroles(ctx):
    if ctx.channel.permissions_for(ctx.author).manage_roles:
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
    else: await ctx.channel.send("You don't have permission to use that command :sweat_smile: ")


@client.command()
async def linkroles(ctx):
    if ctx.channel.permissions_for(ctx.author).manage_roles:
        cmcs = ctx.message.content.split(" ")[1:]
        rec = discord.utils.get(ctx.guild.roles, name=cmcs[0].replace("_", " "))
        torec = discord.utils.get(ctx.guild.roles, name=cmcs[1].replace("_", " "))
        file = open('linkroles.json', 'r+')
        guilds = json.load(file)
        sid = str(ctx.guild.id)
        guild = guilds.get(sid) or []
        add = True
        for x in guild:
            if rec.name == x.split(":")[0] and torec.name == x.split(":")[1]:
                add = False
                guild.remove(x)
        if add:
            guild.add(rec.name + ":" + torec.name)
        guilds.update({sid:guild})
        file = open('linkroles.json', 'w+')
        file.write(json.dumps(guilds))
    else: await ctx.channel.send("You don't have permission to use that command :sweat_smile: ")


@client.command()
async def privatechannels(ctx):
    if ctx.channel.permissions_for(ctx.author).manage_guild and ctx.channel.permissions_for(ctx.author).manage_channels:
        if not ctx.channel.permissions_for(discord.utils.get(ctx.guild.members, id=447268676702437376)).manage_channels:
            await ctx.channel.send("I require the manage channels permission for this.")
            return
        cmc = ctx.message.content.split(" ")[1:]
        if len(cmc) == 0:
            ctx.message.content = "!?help privatechannels"
            await client.process_commands(ctx.message)
            return
        file = open('privatechannels.json', 'r+')
        PCs = json.load(file)
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
                    await ctx.channel.send("Succesfully disallowed free creation by " + role.name + " while freecreation is disabled")
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
                    if int(cmc[0]) > 0 and int(cmc[0]) <= 100:
                        guildPC.update({'max': int(cmc[0])})
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
                await ctx.channel.send("Added owner")
            elif chid in chanlist:
                chanlist.remove(chid)
                guildPC.update({oid: chanlist})
                await ctx.channel.send("Removed owner")
        else: 
            ctx.message.content = "!?help privatechannels"
            await client.process_commands(ctx.message)
            return
        
        PCs.update({gid:guildPC})
        file = open('privatechannels.json', 'w+')
        file.write(json.dumps(PCs))
    else: await ctx.channel.send("You don't have permission to use that command :sweat_smile: ")


@client.command()
async def pchan(ctx):
    if not ctx.channel.permissions_for(discord.utils.get(ctx.guild.members, id=447268676702437376)).manage_channels:
        await ctx.channel.send("I require the manage channels permission for this.")
        return
    cmc = ctx.message.content.split(" ")[1:]
    if len(cmc) == 0:
        ctx.message.content = "!?help pchan"
        await client.process_commands(ctx.message)
        return
    file = open('privatechannels.json', 'r+')
    PCs = json.load(file)
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
    target = await hm.gettarget(ctx, cmc[1])
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
    elif cmc[0].lower() == "kick":
        overwrite = discord.PermissionOverwrite(read_messages=None)
    elif cmc[0].lower() == "superkick":
        overwrite = discord.PermissionOverwrite(read_messages=False)
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
        file = open('privatechannels.json', 'w+')
        file.write(json.dumps(PCs))
        
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
    cmc = ctx.message.content.split(" ")[1:]
    if len(cmc) == 0:
        ctx.message.content = "!?help pchancreate"
        await client.process_commands(ctx.message)
        return
    file = open('privatechannels.json', 'r+')
    PCs = json.load(file)
    gid = str(ctx.guild.id)
    guildPC = PCs.get(gid)
    
    testfc = True
    deny = False
    for x in ctx.author.roles:
        rid = str(x.id)
        if guildPC.get(rid):
            testfc = False
            deny = False
            break
        elif guildPC.get(rid) == False:
            deny = True
        
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
    file = open('privatechannels.json', 'w+')
    file.write(json.dumps(PCs))
    
@client.command()
async def pchandelete(ctx):
    if not ctx.channel.permissions_for(discord.utils.get(ctx.guild.members, id=447268676702437376)).manage_channels:
        await ctx.channel.send("I require the manage channels permission for this.")
        return
    cmc = ctx.message.content.split(" ")[1:]
    if len(cmc) == 0:
        ctx.message.content = "!?help pchandelete"
        await client.process_commands(ctx.message)
        return
    file = open('privatechannels.json', 'r+')
    PCs = json.load(file)
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
    file = open('privatechannels.json', 'w+')
    file.write(json.dumps(PCs))
    
@client.command()
async def pchanowned(ctx):
    file = open('privatechannels.json', 'r+')
    PCs = json.load(file)
    gid = str(ctx.guild.id)
    guildPC = PCs.get(gid)
    chans = guildPC.get(str(ctx.author.id))
    
    if not chans:
        await ctx.channel.send("You don't own any channels in this server/guild.")
        return
    s = "Channels you own in this server/guild: "
    for x in chans:
        chan = discord.utils.get(ctx.guild.channels, id=int(x))
        s += '\n' + chan.mention + ' '
    await ctx.channel.send(s)
    
    
@client.command()
async def setprefix(ctx):
    if ctx.channel.permissions_for(ctx.author).manage_guild:
        np = ctx.message.content.split(' ', 1)[1]
        hm.setprefix(str(ctx.guild.id), np)
        await ctx.channel.send("prefix changed to `{}`".format(np))
    else: await ctx.channel.send("You don't have permission to use that command :sweat_smile: ")
        
        
@client.command()
async def roll(ctx):
    cmcs = ctx.message.content.split(" ")[1:]
    if len(cmcs) == 0:
        await ctx.channel.send("You rolled a " + str(random.randint(1, 6)) + ".")
    else:
        nsp = NumericStringParser()
        nums = cmcs[0].split("d")
        cha = 0
        if "+" in nums[1] or "-" in nums[1] and nsp.eval(nums[1]):
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
            n = nsp.eval(nums[1])
        except: return
        dice = int(nums[0] or 1)
        cl = 1994
        mes = 1
        if dice > 1000//len(str(n)):
            await ctx.channel.send("Too many dice")
            return
        for _11 in range(dice):
            rand = random.randint(1, n) + cha
            total += rand
            s += str(rand) + " "
        if dice > 1:
            if len(cmcs)>1:
                s += str(math.trunc(nsp.eval(str(total) + ''.join(cmcs[1:]))))
            else:
                s += str(total)
        if dice < 2:
            await ctx.channel.send("You rolled a " + s.strip() + ".")
        elif len(s) <= mes * cl:
            while(len(s) > cl):
                await ctx.channel.send("```" + s[:cl] + "```")
                s = s[cl:]
            await ctx.channel.send("```" + s + "```")
        else:
            await ctx.channel.send("```" + s[:cl] + "```")


@client.command()
async def rps(ctx):
    opts = ["Rock", "Paper", "Scissors"]
    cmcs = ctx.message.content.split(" ")[1]
    rand = random.randint(0,2)
    ic = opts[rand]
    win = ic + " wins!"
    if cmcs == "✊" or "Rock" in cmcs or "rock" in cmcs:
        if rand == 2: win = cmcs + " wins!"
        elif rand == 1: win = ic + " wins!"
        else: win = "It's a tie!"
    elif cmcs == "✂" or "Scissors" in cmcs or "scissors" in cmcs:
        if rand == 1: win = cmcs + " wins!"
        elif rand == 0: win = ic + " wins!"
        else: win = "It's a tie!"
    elif cmcs == "📰" or "Paper" in cmcs or "paper" in cmcs:
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
async def emojify(ctx):
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
    await ctx.message.delete()
    await ctx.channel.send(s[:2000])
    
    
@client.command()
async def pfp(ctx):
    if ctx.message.mentions:
        user = ctx.message.mentions[0]
    else: user = ctx.author
    await ctx.channel.send(user.avatar_url)
    
    
@client.command()
async def rolecount(ctx):
    cmc = ctx.message.content.split(" ")[1:]
    s = "​"
    for x in cmc:
        role = discord.utils.get(roles, name=x.replace("_", " "))
        if role:
            num = 0
            for y in ctx.guild.members:
                if role in y.roles:
                    num += 1
            s += "\n" + x.replace("_", " ") + ": " + str(num)
    await ctx.channel.send(s)


@client.command()
async def calc(ctx):
    cmc = ctx.message.content.split(" ", 1)[1].replace(",", "")
    nsp = NumericStringParser()
    await ctx.channel.send("{:,}".format(nsp.eval(hm.wordnumtonum(cmc, str(ctx.author.id)))))


@client.command()
async def wa(ctx):
    cmc = ctx.message.content.split(' ', 1)[1]
    r = requests.get('http://api.wolframalpha.com/v1/result?appid=U7QXJX-VRAQKV8L5A&i=' + cmc)
    await ctx.channel.send(r.text)


@client.command()
async def palindrome(ctx):
    cmc = ctx.message.content.split(' ', 1)[1].lower().replace(' ', '')
    for x, y in zip(cmc, cmc[::-1]):
        if not x == y:
            await ctx.channel.send("No")
            return
    await ctx.channel.send("Yes")
    

@client.command()
async def dtm(ctx):
    cmc = ctx.message.content.split(" ", 2)[1:]
    if len(cmc) == 2:
        if hm.isdigit(cmc[1]):
            await ctx.channel.send((await client.get_channel(int(cmc[1])).get_message(int(cmc[0]))).jump_url)
        else: 
            await ctx.channel.send((await discord.utils.get(client.get_all_channels(), mention=cmc[1]).get_message(int(cmc[0]))).jump_url)
    elif len(cmc) == 1:
        await ctx.channel.send((await ctx.channel.get_message(int(cmc[0]))).jump_url)
    await ctx.message.delete()
    
    
@client.command()
async def morse(ctx):
    cmc = ctx.message.content.replace(' / ', '  ').replace(' / / ', '    ').upper().split(' ', 1)[1]
    morse = False
    for x in cmc:
        if not x == '.' and not x == '-' and not x == ' ' and not x == '/':
            morse = True
    if morse:
        await ctx.channel.send('```' + hm.texttomorse(cmc) + '```')
        return
    await ctx.channel.send('```' + hm.morsetotext(cmc) + '```')


@client.command()
async def invite(ctx):
    l = link.format(client.user.id)
    await ctx.channel.send("<{}>".format(l))
    

@client.command()
async def wordcount(ctx):
    cmc = ctx.message.content.split(" ")[1:]
    after = None
    before = None
    target = None
    for x in range(0, len(cmc)):
        if cmc[x].lower() == "after":
            if hm.isdigit(cmc[x+1]):
                after = await ctx.channel.get_message(int(cmc[x+1]))
                if not after:
                    await ctx.channel.send("Invalid message id, perhaps you copied the user id instead of the message id?")
                    return
        elif cmc[x].lower() == "before":
            if hm.isdigit(cmc[x+1]):
                before = await ctx.channel.get_message(int(cmc[x+1]))
                if not before:
                    await ctx.channel.send("Invalid message id, perhaps you copied the user id instead of the message id?")
                    return
        elif not target:
            if '#' in cmc[x]:
                target = discord.utils.get(ctx.guild.members, name=cmc[x].split('#')[0], discriminator=cmc[x].split('#')[1])
            elif hm.isdigit(cmc[x]):
                target = discord.utils.get(ctx.guild.members, id=int(cmc[x]))
            else:
                target = discord.utils.get(ctx.guild.members, mention=cmc[x])
    num = 0
    async for x in ctx.channel.history(limit=None, after=after, before=before):
        if x.author == target or target == None:
            num += len(x.content) - len(x.content.replace(" ", "")) + 1
    aftermsg = " after " + after.author.name + "'s specified message" if after else " before " + before.author.name + "'s specified message" if before else ""
    trg = target.name if target else "Everyone"
    await ctx.channel.send(trg + " has sent " + str(num) + " words in this channel"+ aftermsg +".")
    await ctx.message.delete()
    
    
@client.command()
async def counting(ctx):
    if ctx.channel.permissions_for(ctx.author).manage_guild:
        cmc = ctx.message.content.split(" ")[1:]
        #initialize variables
        channel = None
        increment = None
        start = None
        #arguments to variables
        for x in range(0, len(cmc)):
            if not channel:
                channel = await hm.getchannel(ctx, cmc[x])
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
        file = open('counting.json', 'r+')
        c = json.load(file)
        #load dictionary
        gid = str(ctx.guild.id)
        gc = c.get(gid) or {}
        cid = str(channel.id)
        cc = gc.get(cid) or {}
        #store in dictionary
        cc.update({'inc':increment, 'current':start})
        gc.update({cid:cc})
        c.update({gid:gc})
        #write to file
        file = open('counting.json', 'w+')
        file.write(json.dumps(c))
    else: await ctx.channel.send("You don't have permission to use that command :sweat_smile: ")
        
@client.command()
async def killbot(ctx):
    if str(ctx.author) == "Tiln#0416":
        await ctx.message.delete()
        await client.logout()


async def pm_peeps():
    tonline = True
    eionline = True
    while(True):
        peeps = discord.utils.get(client.guilds, id=455380663013736479).members
        Andy = discord.utils.get(peeps, id=346503259189411840)
        Tiln = discord.utils.get(peeps, id=115707766714138627)
        TilnBot = discord.utils.get(peeps, id=447268676702437376)
        if str(TilnBot.status) == "offline":
            if tonline == True:
                await Andy.send("Tiln's gen-bot has gone offline")
                await Tiln.send("Tiln's gen-bot has gone offline")
                tonline = False
        elif tonline == False:
            tonline = True
        EggInc = discord.utils.get(peeps, id=447654351595503616)
        if str(EggInc.status) == "offline":
            if eionline == True:
                await Andy.send("Egg, Inc. bot has gone offline")
                await Tiln.send("Egg, Inc. bot has gone offline")
                eionline = False
        elif eionline == False:
            eionline = True
        await asyncio.sleep(10)


file = open(os.path.dirname(__file__) + "/../tok.txt")
client.run(file.readline())
file.close




