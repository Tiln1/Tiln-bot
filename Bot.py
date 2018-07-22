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

import platform

import discord
from discord.ext import commands
from discord.ext.commands import Bot

from TilnBot.calceval import NumericStringParser
from TilnBot.otherStuff import HelpMethods
from _ast import If
from test.test_nntplib import bypass_context
from django.contrib.auth.context_processors import auth

client = Bot(description="Tiln's bot", command_prefix="!?", pm_help = False)
client.remove_command('help')

hm = HelpMethods()
asc = ['', '', '', '', '', '', '', '', '    ', '', '', '\n', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ' ', '!', '"', '#', '$', '%', '&', '\'', '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '[', '\\', ']', '^', '_', "`", 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ' ', '¡', '¢', '£', '¤', '¥', '¦', '§', '¨', '©', 'ª', '«', '¬', '­', '®', '¯', '°', '±', '²', '³', '´', 'µ', '¶', '·', '¸', '¹', 'º', '»', '¼', '½', '¾', '¿', 'À', 'Á', 'Â', 'Ã', 'Ä', 'Å', 'Æ', 'Ç', 'È', 'É', 'Ê', 'Ë', 'Ì', 'Í', 'Î', 'Ï', 'Ð', 'Ñ', 'Ò', 'Ó', 'Ô', 'Õ', 'Ö', '×', 'Ø', 'Ù', 'Ú', 'Û', 'Ü', 'Ý', 'Þ', 'ß', 'à', 'á', 'â', 'ã', 'ä', 'å', 'æ', 'ç', 'è', 'é', 'ê', 'ë', 'ì', 'í', 'î', 'ï', 'ð', 'ñ', 'ò', 'ó', 'ô', 'õ', 'ö', '÷', 'ø', 'ù', 'ú', 'û', 'ü', 'ý', 'þ' ]
emojAN = ['🇦', '🇧', '🇨', '🇩', '🇪', '🇫', '🇬', '🇭', '🇮', '🇯', '🇰', '🇱', '🇲', '🇳', '🇴', '🇵', '🇶', '🇷', '🇸', '🇹', '🇺', '🇻', '🇼', '🇽', '🇾', '🇿', '0⃣', '1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣']
#:hash: :exclamation: :question: :heavy_plus_sign: :heavy_minus_sign: :heavy_multiplication_x: :heavy_division_sign: :heavy_dollar_sign:
emojmisc = ['🔥', '❗', '❓', '➕', '➖', '*⃣', '➗', '💲']
emojdoub = ['🆎', '🆑', '🆔', '🆖', '🆗', '🆚', '🚾', '‼', '⁉', '🆕', '🆘', '🆒', '🆓', '🔟']
cmds = ['help', 'uroles', 'pin', 'react', 'clearreactions', 'purge', 'collectpoll', 'exclusivizeroles', 'timedroles', 'linkroles', 'roll', 'rps', 'emojify', 'pfp', 'rolecount', 'calc']



#:a: :b: :information_source: :pisces: :m: :scorpio: :virgo: :capricorn: :o2: :o: :parking: :Aries: :negative_squared_cross_mark: :x: :grey_exclamation: :grey_question:\

@client.event
async def on_ready():
    print('Logged in as '+client.user.name+' (ID:'+client.user.id+') | Connected to '+str(len(client.servers))+' servers | Connected to '+str(len(set(client.get_all_members())))+' users')
    print('--------')
    print('Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__, platform.python_version()))
    print('--------')
    print('Use this link to invite {}:'.format(client.user.name))
    print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=268774464'.format(client.user.id))
    print('--------')
    await client.change_presence(game=discord.Game(name="!?help for help")) #This is buggy, let us know if it doesn't work.
    await pm_peeps()
    return


@client.event
async def on_message(message):
    
#     if message.server.id == "381581408491012097":
#         if message.channel.id == "447415555557818368":
#             if len(message.content) > 0:
#                 await client.delete_message(message)
    rolesset = False
    
    if message.channel == client.get_channel("465333717871886336") and not message.content.startswith("!?emojify") and not message.content.startswith("!?react") and not message.content.startswith("!?purge") and not message.content.startswith("!?calc"):
            message.content = "!?emojify " + message.content.replace("\n", "")
    if message.channel == client.get_channel("465333717871886336") and message.content.startswith("!?calc"):
        nsp = NumericStringParser()
        result = ""
        try: result = nsp.eval(message.content.split(" ", 1)[1])
        except: ""
        if result:
            message.content = "!?emojify " + str(result)
    for x in message.content.split("\n"):
        mc = x.lower()
        rp = re.compile(r"\d*d(?:\d|\^|\*|-|\+| )+")
        if x.startswith("!?"):
            if not rolesset:
                global roles
                roles = message.server.roles
            rolesset = True
            
            command=x.lower().split(" ", 1)[0]
            for y in range(10, -1, -1):
                x = x.replace(" "*(2**y+1), " ")
            message.content=command+x[len(command):]
            cmd = message.content.split(" ")[0][2:]
            if not hm.cmddisabled(message.server.id, cmd):
                await client.process_commands(message)
            else: await client.say("The command \"" + cmd + "\" is disabled in this server.")
        elif rp.match(x):
            message.content="!?roll "+x
            cmd = message.content.split(" ", 1)[0][2:]
            if not hm.cmddisabled(message.server.id, cmd):
                await client.process_commands(message)
        elif ("+" in mc or "-" in mc or "/" in mc or "*" in mc or "^" in mc or "sin(" in mc or "cos(" in mc or "tan(" in mc or "exp(" in mc or "abs(" in mc or "trunc(" in mc or "round(" in mc or "sqrt(" in mc or "sgn(" in mc or "mod(" in mc) and not hm.cmddisabled(message.server.id, "calc") and not message.content.startswith("+") and not message.content.startswith("-") and not message.content.startswith("*") and not message.content.startswith("/"):
            nsp = NumericStringParser()
            result = ""
            try: result = nsp.eval(mc)
            except: ""
            if result:
                await client.send_message(message.channel, str(result)[:2000])
        
            
            
@client.event
async def on_member_update(before, after):
    if before.roles == after.roles:
        return
    sid = after.server.id
    
    file = open('exclusiveroles.csv', 'r')
    exservers = file.read().split('\n')
    file.close() 
    exrg = None
    for x in exservers:
        if x.startswith(sid):
            exrg = x
    
    file = open('linkedroles.csv', 'r')
    linkservers = file.read().split('\n')
    file.close()
    sid = after.server.id
    linkrp = None
    for x in linkservers:
        if x.startswith(sid):
            linkrp = x
    if linkrp == None:
        return
    #role added
    for x in after.roles:
        if linkrp:
            for y in linkrp.split(',')[1:]:
                if x.name == y.split(':')[0] and not x in before.roles:
                    await client.add_roles(after, discord.utils.get(after.server.roles, name=y.split(":")[1]))
        if exrg:
            for y in exrg.split(',')[1:]:
                if x.name in y.split(':') and not x in before.roles:
                    rtr = []
                    for z in y.split(':'):
                        if not z == x.name:
                            rtr.append(discord.utils.get(after.server.roles, name=z))
                    await client.remove_roles(after, *tuple(rtr))
                    return
                    
    #role removed
    for x in before.roles:
        if linkrp:
            for y in linkrp.split(',')[1:]:
                if x.name == y.split(':')[0] and not x in after.roles:
                    await client.remove_roles(after, discord.utils.get(after.server.roles, name=y.split(":")[1]))
                    return


import requests
import justext
@client.command(pass_context=True)
async def ping(ctx):
    if str(ctx.message.author) == "Tiln#0416":
        response = requests.get("http://www.crunchyroll.com/yuruyuri")
        paragraphs = justext.justext(response.content, justext.get_stoplist("English"))
        s = "```"
        start = False
        for p in paragraphs:
            if p.text.startswith("YuruYuri Season") and start == False:
                start = True
            elif p.text == "Viewers Also Liked":
                break
            if start:
                s += p.text + "\n"
        await client.say(s + "```")
    else:
        msg = await client.say("Pong!")
        time = math.trunc((msg.timestamp - ctx.message.timestamp).total_seconds() * 1000)
        await client.edit_message(msg, "Pong! `" + str(time) + " ms`")
    
    
    
@client.command(pass_context=True)
async def help(ctx):
    com = ctx.message.content.lower().split(" ")
    base = False
    if len(com)>1:
        c = com[1]
        if c == "disable":
            await client.say("```!?disable *commandstodisable\n!?disable role1 role2 role3```")
        elif c == "enable":
            await client.say("```!?enable *commandstoenable\n!?enable all```")
        elif c == "uroles" and not hm.cmddisabled(ctx.message.server.id, c):
            await client.say("```!?"+c+" @member *rolestoadd|*rolestoremove\nExample: !?"+c+" Farmer_III Kilofarmer_III Megafarmer_III Gigafarmer_III|Gigafarmer_II Eggs```")
        elif c == "pin" and not hm.cmddisabled(ctx.message.server.id, c):
            await client.say("```!?"+c+" <@member>\n<> Means optional ```")
        elif c == "react" and not hm.cmddisabled(ctx.message.server.id, c):
            if len(com) > 2:
                b = com[2]
                if b == "repeats":
                    await client.say("```diff\n3 on all letters;\n-j,k,q,z\n+a, a, d, e, e, h, i, i, l, m, n, o, r, s, t, t, !, ?, *, *```")
                    return
                elif b == "doubles":
                    await client.say("```ab, cl, id, ng, ok, vs, wc, !!, !?, new, sos, cool, free, 10```")
                    return
                elif b == "misc":
                    await client.say("```+, -, *, /, $, !, ?```")
                    return
            await client.say("```!?"+c+" <@member/messageid> *reactions\n<> Means optional and skippable```")
        elif c == "clearreactions" and not hm.cmddisabled(ctx.message.server.id, c):
            await client.say("```!?"+c+" <@member/messageid/number of messages>\n<> Means optional\n```")
        elif c == "roll" and not hm.cmddisabled(ctx.message.server.id, c):
            await client.say("```!?"+c+" <<number of dice>d[how large of a dice][plus or minus some number to add to each roll]> <something to do to the total>\nExample: !?"+c+" 5d6+1 +1```")
        elif c == "rps" and not hm.cmddisabled(ctx.message.server.id, c):
            await client.say("```!?"+c+" [Rock/Paper/Scissors]```")
        elif c == "purge" and not hm.cmddisabled(ctx.message.server.id, c):
            await client.say("```!?"+c+" [number of messages]\nor for deleting a single user's messsages:\n!?"+c+" [@member/userid] [number of messages]\nor for deleting messages except by a certain user:\n!?"+c+" [@member/userid]! [number of messages]```")
        elif c == "collectpoll" and not hm.cmddisabled(ctx.message.server.id, c):
            await client.say("```!?"+c+" channelid [number of messages that consist of the poll]```")
        elif c == "timedroles" and not hm.cmddisabled(ctx.message.server.id, c):
            await client.say("```!?timedroles"+c+" [time][y/o/w/d/h/m/s] role_name\n!?"+c+" 1y the_best_role```")
        elif c == "emojify" and not hm.cmddisabled(ctx.message.server.id, c):
            await client.say("```!?"+c+" [message]```")
        elif c == "pfp" and not hm.cmddisabled(ctx.message.server.id, c):
            await client.say("```!?"+c+"```")
        elif c == "rolecount":
            await client.say("```!?rolecount *roles")
        elif c == "misc":
            await client.say("```!?roll rolls some dice\n!?rps plays rock paper scissors\n!?emojify emojifies a message\n!?pfp returns your profile picture\n!?calc returns the calculation results\n```")
        else: await client.say("!?"+c+" is not currently a command or is disabled")
    else: base = True
    s = ""
    if base:
        s += "```!?help Displays this command\n!?help misc for misc commands\n!?collectpoll collects a poll\n!?rolecount counts the number of people in the specified role(s)\n"
        if ctx.message.channel.permissions_for(ctx.message.author).manage_server:
            s += "!?enable enables commands\n!?disable disables commands\n"
        if ctx.message.channel.permissions_for(ctx.message.author).add_reactions and ctx.message.channel.permissions_for(discord.utils.get(ctx.message.server.members, id="447268676702437376")).add_reactions:
            s += "!?react adds reactions to the most recent message\n"
        if ctx.message.channel.permissions_for(ctx.message.author).manage_roles and ctx.message.channel.permissions_for(discord.utils.get(ctx.message.server.members, id="447268676702437376")).manage_roles:
            s += "!?uroles adds and or removes role(s) from a member\n!?timedroles adds roles based on their time in the server\n"
        if ctx.message.channel.permissions_for(ctx.message.author).manage_messages and ctx.message.channel.permissions_for(discord.utils.get(ctx.message.server.members, id="447268676702437376")).manage_messages:
            s += "!?purge purges the most recent n messages or n messages by a specified user checking only the most 100 recent messages\n!?pin pins the most recent message\n!?clearreactions clears the reactions of the most recent message\n"
        s += "!?help [command] for help on that command```"
        await client.say(s)


@client.command(pass_context=True)
async def disable(ctx):
    if ctx.message.channel.permissions_for(ctx.message.author).manage_server:
        file = open('servers.csv', 'r')
        servers = file.read().split("\n")
        file.close()
        sid = ctx.message.server.id
        server = None
        s = ""
        for x in servers:
            if x.startswith(sid):
                server = x
            else:
                s += x + "\n"
    
        if not server:
            server = sid
        
        cmc = ctx.message.content.split(" ")
        if len(cmc) > 1:
            for x in cmc[1:]:
                if x in cmds:
                    disableable = True
                    for y in server.split(","):
                        if y == x:
                            disableable = False
                            break
                    if disableable:
                        server += "," + x
                elif x == "all":
                    for y in cmds:
                        disableable = True
                        for z in server.split(","):
                            if z == y:
                                disableable = False
                                break
                        if disableable:
                            server += "," + y
                    break
        else: return
        s += server
        file = open('servers.csv', 'w')
        file.write(s)
        file.close()
    else: await client.say("You don't have permission to use that command :sweat_smile: ")
    

@client.command(pass_context=True)
async def enable(ctx):
    if ctx.message.channel.permissions_for(ctx.message.author).manage_server:
        file = open('servers.csv', 'r')
        servers = file.read().split("\n")
        file.close()
        sid = ctx.message.server.id
        server = None
        s = ""
        for x in servers:
            if x.startswith(sid):
                server = x
            else:
                s += x + "\n"
        if not server: return
        cmc = ctx.message.content.split(" ")
        if len(cmc) > 1:
            for x in cmc[1:]:
                if x in cmds:
                    server = server.replace("," + x, "")
                elif x == "all":
                    for y in cmds:
                        server = server.replace("," + y, "")
                    break
        else: return
        s += server
        file = open('servers.csv', 'w')
        file.write(s)
        file.close()
    else: await client.say("You don't have permission to use that command :sweat_smile: ")
    

@client.command(pass_context=True)
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
            
            
@client.command(pass_context = True)
async def pin(ctx):
    if ctx.message.channel.permissions_for(ctx.message.author).manage_messages:
        pinned = False;
        if len(ctx.message.content.split(" ")) > 1:
            mid = ctx.message.content.split(" ")[1]
            if mid.isdigit():
                if int(mid) > 10000:
                    await client.pin_message(await client.get_message(ctx.message.channel, mid))
                    await client.delete_message(ctx.message)
                    return
        async for x in client.logs_from(ctx.message.channel):
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
        if not pinned: await client.say("The user you are trying to pin is not recent enough or does not exist.")
    else: await client.say("You don't have permission to use that command :sweat_smile: ")
    await client.delete_message(ctx.message)


@client.command(pass_context = True)
async def react(ctx):
    if ctx.message.channel.permissions_for(ctx.message.author).add_reactions:
        emojdup = [discord.utils.get(client.get_all_emojis(), name="a_", id="448623901027860500"), discord.utils.get(client.get_all_emojis(), name="a_", id="448623288160223242"), discord.utils.get(client.get_all_emojis(), name="a_", id="448623554292875266"), u'🅰', discord.utils.get(client.get_all_emojis(), name="b_", id="448623288177000448"), u'🅱', discord.utils.get(client.get_all_emojis(), name="c_", id="448623288185257994"), discord.utils.get(client.get_all_emojis(), name="c_", id="448623554582282240"), discord.utils.get(client.get_all_emojis(), name="d_", id="448623287782604801"), discord.utils.get(client.get_all_emojis(), name="d_", id="448623900834922500"), discord.utils.get(client.get_all_emojis(), name="d_", id="448623554611773440"), discord.utils.get(client.get_all_emojis(), name="e_", id="448623554582282260"), discord.utils.get(client.get_all_emojis(), name="e_", id="448623980753190913"), discord.utils.get(client.get_all_emojis(), name="e_", id="448623288445435914"), discord.utils.get(client.get_all_emojis(), name="e_", id="448623900889186317"), discord.utils.get(client.get_all_emojis(), name="f_", id="448623288189714442"), discord.utils.get(client.get_all_emojis(), name="f_", id="448623554582544384"), discord.utils.get(client.get_all_emojis(), name="g_", id="448623554615836673"), discord.utils.get(client.get_all_emojis(), name="g_", id="448623288109891585"), discord.utils.get(client.get_all_emojis(), name="h_", id="448623554544664586"), discord.utils.get(client.get_all_emojis(), name="h_", id="448623288214880296"), u'♓', discord.utils.get(client.get_all_emojis(), name="i_", id="448623901040443392"), discord.utils.get(client.get_all_emojis(), name="i_", id="448623288277532692"), discord.utils.get(client.get_all_emojis(), name="i_", id="448623554611642368"), u'ℹ', discord.utils.get(client.get_all_emojis(), name="j_", id="448623287833198603"), discord.utils.get(client.get_all_emojis(), name="k_", id="448623288193646609"), discord.utils.get(client.get_all_emojis(), name="l_", id="448623901040443402"), discord.utils.get(client.get_all_emojis(), name="l_", id="448623554670362625"), discord.utils.get(client.get_all_emojis(), name="l_", id="448623288210686003"), u'Ⓜ', u'♏', u'♍', discord.utils.get(client.get_all_emojis(), name="n_", id="448623554628419584"), discord.utils.get(client.get_all_emojis(), name="n_", id="448623288197840926"), u'♑', discord.utils.get(client.get_all_emojis(), name="o_", id="448623288487247882"), u'🅾', u'⭕', discord.utils.get(client.get_all_emojis(), name="p_", id="448623288466276382"), u'🅿', discord.utils.get(client.get_all_emojis(), name="q_", id="448623288281726996"), discord.utils.get(client.get_all_emojis(), name="r_", id="448625035985420289"), discord.utils.get(client.get_all_emojis(), name="r_", id="448623287929667596"), discord.utils.get(client.get_all_emojis(), name="r_", id="448623900771745793"), discord.utils.get(client.get_all_emojis(), name="s_", id="448623554590932992"), discord.utils.get(client.get_all_emojis(), name="s_", id="448623288210554880"), discord.utils.get(client.get_all_emojis(), name="s_", id="448623901044375552"), discord.utils.get(client.get_all_emojis(), name="t_", id="448623287866490881"), discord.utils.get(client.get_all_emojis(), name="t_", id="448623901220536331"), discord.utils.get(client.get_all_emojis(), name="t_", id="448623980849659926"), discord.utils.get(client.get_all_emojis(), name="t_", id="448623554498527233"), discord.utils.get(client.get_all_emojis(), name="u_", id="448623554590933002"), discord.utils.get(client.get_all_emojis(), name="u_", id="448623288470601738"), discord.utils.get(client.get_all_emojis(), name="v_", id="448623288055496725"), u'♈', discord.utils.get(client.get_all_emojis(), name="w_", id="448623288214749187"), discord.utils.get(client.get_all_emojis(), name="w_", id="448623554519629825"), '❎', '❌', discord.utils.get(client.get_all_emojis(), name="y_", id="448623554636808193"), discord.utils.get(client.get_all_emojis(), name="y_", id="448623288210554900"), discord.utils.get(client.get_all_emojis(), name="z_", id="448623288512675840"), u'❕', u'❔', u'✳', u'✖']
        doub = ["ab", "cl", "id", "ng", "ok", "vs", "wc", "!!", "!?", "new", "sos", "cool", "free"]
        dup = ["a", "a", "a", "a", "b", "b", "c", "c", "d", "d", "d", "e", "e", "e", "e", "f", "f", "g", "g", "h", "h", "h", "i", "i", "i", "i", "j", "k", "l", "l", "l", "m", "m", "m", "n", "n", "n", "o", "o", "o", "p", "p", "q", "r", "r", "r", "s", "s", "s", "t", "t", "t", "t", "u", "u", "v", "v", "w", "w", "x", "x", "y", "y", "z", "!", "?", "*", "*"]
        #dup = ["a", "b", "i", 'h', "m", "m", "m", "n", "o", "o", "p", "v", "x", "x", "!", "?", "*", "*"]
        duptrans = []
        com = ctx.message.content.split(" ")
        num = 1
        ment = False
        mid = False
        mem = ""
        if com[1].isdigit():
            if int(com[1]) > 1000000000:
                num = 2
                mid = True
        elif ctx.message.mentions:
            num = 2
            ment = True
            mem = ctx.message.mentions[0]
        async for x in client.logs_from(ctx.message.channel):
            if mid:
                x = await client.get_message(ctx.message.channel, com[1])
            if (not x.content.startswith("!?react") and (not ment or x.author == mem)) or mid:
                emoji = []
                try:
                    await client.delete_message(ctx.message)
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
                        mes = discord.utils.get(client.get_all_emojis(), name=com[y].strip("<>").split(":")[1], id=com[y].strip("<>").split(":")[2])
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
                    await client.add_reaction(x, y)
                return
        await client.say("The user you are trying to react to is not recent enough or does not exist.")
        await client.delete_message(ctx.message)
    else: await client.say("You don't have permission to use that command :sweat_smile: ")
    
    
@client.command(pass_context = True)
async def clearreactions(ctx):
    if ctx.message.channel.permissions_for(ctx.message.author).manage_messages:
        mess = ""
        com = ctx.message.content.split(" ")
        mid = ""
        mem = ""
        if len(com) > 1:
            mid = com[1]
        if mid.isdigit():
            if int(mid) > 10000:
                await client.clear_reactions(await client.get_message(ctx.message.channel, mid))
                await client.delete_message(ctx.message)
                return
            else:
                mid = int(mid)
        elif ctx.message.mentions:
            mem = ctx.message.mentions[0]
        else: mid = 0
        num = 0
        async for x in client.logs_from(ctx.message.channel):
            if not x.content == "!?clearreactions" and x.reactions and (x.author == mem or not mem):
                mess = x
                num += 1
                await client.clear_reactions(mess)
                if num >= mid or not mid:
                    break
    else: await client.say("You don't have permission to use that command :sweat_smile: ")
    await client.delete_message(ctx.message)
    

@client.command(pass_context = True)
async def purge(ctx):
    if ctx.message.channel.permissions_for(ctx.message.author).manage_messages:
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
        if cmc[1].isdigit():
            if int(cmc[1]) > 100000:
                isufi = True
                uid = cmc[1]
        if ctx.message.mentions or isufi:
            arg2 = ""
            if len(cmc) > 2:
                arg2 = cmc[2]
            else: arg2 = "99"
            limit = 100
            if arg2.isdigit():
                limit = int(arg2) + 1
            if isufi:
                if not ctx.message.author == ctx.message.server.get_member(uid):
                    await client.delete_message(ctx.message)
                    limit -= 1
            else:
                if not ctx.message.author == ctx.message.mentions[0]:
                    await client.delete_message(ctx.message)
                    limit -= 1
        elif cmc[1].isdigit():
            limit = int(cmc[1]) + 1
        else:
            await client.say("No number of messages nor user specified")
            return
        prevlimit = -552
        while limit > 0:
            num = 0
            mess = []
            async for x in client.logs_from(ctx.message.channel):
                t = (datetime.utcnow() - x.timestamp).total_seconds()
                if t < 1200000 and not x.pinned:
                    if isufi:
                        if x.author == ctx.message.server.get_member(uid) and not abtu:
                            mess.append(x)
                            num += 1
                            if num >= limit:
                                break
                        elif not x.author == ctx.message.server.get_member(uid) and abtu:
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
                    await client.delete_message(x)
                    num += 1
                    if num >= 1000 or num >= limit:
                        limit = 0
                        break
            if len(mess) > 1:
                await client.delete_messages(mess)
            elif len(mess) == 1:
                await client.delete_message(mess[0])
            limit -= num
            if prevlimit == limit: break
            prevlimit = limit
    else: await client.say("You don't have permission to use that command :sweat_smile: ")
    

@client.command(pass_context = True)
async def collectpoll(ctx):
    cmc = ctx.message.content.split(" ");
    num = 1
    if len(cmc) > 2:
        if cmc[2].isdigit():
            num = int(cmc[2]) or 1
    i = 0
    dic = {}
    async for x in client.logs_from(client.get_channel(cmc[1])):
        s = "​"
        if x.reactions:
            i += 1
            mes = x.content.split("\n")
            for y in x.reactions:
                for z in mes:
                    if str(y.emoji) in z:
                        dic.update({z: y.count-1})
                        break
                if not dic:
                    s += "\n" + str(y.emoji) + ": " + str(y.count-1)
            if not dic:
                await client.say(s)
            if i >= num:
                break
    if dic:
        with open('poll.csv', 'w') as file:
            for k in sorted(dic, key=dic.get, reverse=True):
                #s += k + ": " + str(dic[k]) + "\n"
                file.write(str(k.replace(",", "").encode("utf-8")) + "," + str(dic[k]) + "\n")
        await client.send_file(ctx.message.channel, "poll.csv")
    

@client.command(pass_context = True)
async def exclusivizeroles(ctx):
    if ctx.message.channel.permissions_for(ctx.message.author).manage_roles:
        cmcs = ctx.message.content.split(" ")[1:]
        exroles = []
        strexroles = []
        for x in cmcs:
            r = discord.utils.get(ctx.message.server.roles, name=x.replace("_", " "))
            if not r:
                await client.say(x + " is not recognized as a valid role.")
                return
            else: exroles.append(r)
            strexroles.append(x.replace("_", " "))
        file = open('exclusiveroles.csv', 'r')
        servers = file.read().split("\n")
        file.close()
        sid = ctx.message.server.id
        server = ""
        s = ""
        for x in servers:
            if x.startswith(sid):
                server = x
            else:
                s += x + "\n"
        if not server:
            server = str(sid)
        add = True
        for x in server.split(",")[1:]:
            if strexroles == x.split(":"):
                add = False
                server = server.replace("," + x, "")
        if add:
            server += ","
            for x in strexroles:
                server += x + ":"
            server = server[:-1]
        s += server
        file = open('exclusiveroles.csv', 'w')
        file.write(s)
        file.close()
    else: await client.say("You don't have permission to use that command :sweat_smile: ")

        
@client.command(pass_context = True)
async def timedroles(ctx):
    if ctx.message.channel.permissions_for(ctx.message.author).manage_roles:
        cmc = ctx.message.content.split(" ")
        ml = ctx.message.server.members
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
            t = (ctx.message.timestamp - m.joined_at).total_seconds()
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
    else: await client.say("You don't have permission to use that command :sweat_smile: ")


@client.command(pass_context = True)
async def linkroles(ctx):
    if ctx.message.channel.permissions_for(ctx.message.author).manage_roles:
        cmcs = ctx.message.content.split(" ")[1:]
        rec = discord.utils.get(ctx.message.server.roles, name=cmcs[0].replace("_", " "))
        torec = discord.utils.get(ctx.message.server.roles, name=cmcs[1].replace("_", " "))
        file = open('linkedroles.csv', 'r')
        servers = file.read().split("\n")
        file.close()
        sid = ctx.message.server.id
        server = ""
        s = ""
        for x in servers:
            if x.startswith(sid):
                server = x
            else:
                s += x + "\n"
        if not server:
            server = str(sid)
        add = True
        for x in server.split(",")[1:]:
            if rec.name == x.split(":")[0] and torec.name == x.split(":")[1]:
                add = False
                server = server.replace("," + x, "")
        if add:
            server += "," + rec.name + ":" + torec.name
        s += server
        file = open('linkedroles.csv', 'w')
        file.write(s)
        file.close()
    else: await client.say("You don't have permission to use that command :sweat_smile: ")

@client.command(pass_context = True)
async def roll(ctx):
    cmcs = ctx.message.content.split(" ")[1:]
    if len(cmcs) == 0:
        await client.say("You rolled a " + str(random.randint(1, 6)) + ".")
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
        n = nsp.eval(nums[1])
        dice = int(nums[0] or 1)
        cl = 1994
        mes = 1
        if dice > (cl + 6 * mes) // 2:
            await client.say("Too many dice")
            return
        for _11 in range(dice):
            rand = random.randint(1, n) + cha
            total += rand
            s += str(rand) + " "
        if dice > 1:
            if len(cmcs)>2:
                s += str(math.trunc(nsp.eval(str(total) + ''.join(cmcs[2:]))))
            else:
                s += str(total)
        if dice < 2:
            await client.say("You rolled a " + s.strip() + ".")
        elif len(s) <= mes * cl:
            while(len(s) > cl):
                await client.say("```" + s[:cl] + "```")
                s = s[cl:]
            await client.say("```" + s + "```")
        else:
            await client.say("```" + s[:cl] + "```")


@client.command(pass_context = True)
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
    await client.say("You chose " + cmcs + ". I chose " + ic + ".\n" + win)
    

@client.command(pass_context = True)
async def emojify(ctx):
    author = ctx.message.author.name
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
        print(x)
        stc = stc.replace(x, "⡉")
    emojimen1 = iter(emojimen)
    
    s = "​"
    for x in stc:
        if x in asc:
            nrep = ord(x.lower())
            if x == " ":
                s += str(discord.utils.get(client.get_all_emojis(), name="space", id="465069460588462090"))
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
                s += str(discord.utils.get(client.get_all_emojis(), name="colon", id="465072882964365312"))
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
    await client.delete_message(ctx.message)
    await client.say(s[:2000])
    
    
@client.command(pass_context = True)
async def pfp(ctx):
    await client.say(ctx.message.author.avatar_url)
    
    
@client.command(pass_context = True)
async def rolecount(ctx):
    cmc = ctx.message.content.split(" ")[1:]
    s = "​"
    for x in cmc:
        role = discord.utils.get(roles, name=x.replace("_", " "))
        if role:
            num = 0
            for y in ctx.message.server.members:
                if role in y.roles:
                    num += 1
            s += "\n" + x.replace("_", " ") + ": " + str(num)
    await client.say(s)


@client.command(pass_context = True)
async def calc(ctx):
    cmc = ctx.message.content.split(" ", 1)[1]
    nsp = NumericStringParser()
    await client.say(nsp.eval(cmc))
    
@client.command(pass_context = True)
async def killbot(ctx):
    if str(ctx.message.author) == "Tiln#0416":
        await client.delete_message(ctx.message)
        await client.logout()


import asyncio
async def pm_peeps():
    tonline = True
    eionline = True
    while(True):
        peeps = discord.utils.get(client.servers, id="455380663013736479").members
        Andy = discord.utils.get(peeps, id="346503259189411840")
        Tiln = discord.utils.get(peeps, id="115707766714138627")
        TilnBot = discord.utils.get(peeps, id="447268676702437376")
        if str(TilnBot.status) == "offline":
            if tonline == True:
                await client.send_message(Andy, "Tiln's gen-bot has gone offline")
                await client.send_message(Tiln, "Tiln's gen-bot has gone offline")
                tonline = False
        elif tonline == False:
            tonline = True
        EggInc = discord.utils.get(peeps, id="447654351595503616")
        if str(EggInc.status) == "offline":
            if eionline == True:
                await client.send_message(Andy, "Egg, Inc. bot has gone offline")
                await client.send_message(Tiln, "Egg, Inc. bot has gone offline")
                eionline = False
        elif eionline == False:
            eionline = True
        await asyncio.sleep(10)


file = open(os.path.dirname(__file__) + "/../tok.txt")
client.run(file.readline())
file.close




