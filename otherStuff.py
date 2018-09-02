'''
Created on May 12, 2018

@author: Tiln
'''

import discord
import json


class HelpMethods(object):
    # :a: :b: :information_source: :pisces: :m: :scorpio: :virgo: :capricorn: :o2: :o: :parking: :Aries: :negative_squared_cross_mark: :x: :grey_exclamation: :grey_question:
    # emojdup = ['🅰', '🅱', 'ℹ', '♓', 'Ⓜ', '♏', '♍', '♑', '🅾', '⭕', '🅿', '♈', '❎', '❌', '❕', '❔', '✳', '✖']
    
    # :ab: :cl: :id: :ng: :ok: :vs: :wc: :bangbang: :interrobang: :new: :sos: :cool: :free: :10: 
    emojdoub = ['🆎', '🆑', '🆔', '🆖', '🆗', '🆚', '🚾', '‼', '⁉', '🆕', '🆘', '🆒', '🆓', '🔟']
    
    def cmddisabled(self, sid, cmd):
        file = open('servers.json', 'r+')
        servers = json.load(file)
        server = servers.get(sid) or []
        for x in server:
            if cmd == x:
                return True
        return False
        

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
                await client.replace_roles(user, *tuple(roles))
                # if rtrnothave: print(rtrnothave)
                if respond:
                    await client.say('Successfully updated role(s)')
                return True
            else: await client.say('Please format it as ' + ctx.message.content.split(' ')[0] + ' @username role')
        else: await client.say("You don't have permission to use that command or that part of that command :sweat_smile: ")
        return False
    
    def wordnumtonum(self, s, uid):
        s = s.lower()
#         p = re.compile('[a-z]')
#         m = re.findall(p, s)
#         for x in m:
#             if not 
#             s = s.replace(x, '(' + x + ')')

#         .replace('ninety', '9').replace('seventy', '7').replace('sixty', '6').replace('fifty', '5').replace('forty', '4').replace('thirty', '3').replace('twenty', '2')
        rpldic = {' ':'', '∞':'infinity', 'infinity':'1.7976931348623157e+308', 'centillion':'*'+str(10**303)+'', 'nonagintillion':str(10**273)+'', 
            'octogintillion':'*'+str(10**243)+'', 'septuagintillion':'*'+str(10**213)+')', 'sexagintillion':'*'+str(10**183)+'', 
            'quinquagintillion':'*'+str(10**153)+'', 'quadragintillion':'*'+str(10**123)+'', 'trigintillion':'*'+str(10**93)+'', 
            'vigintillion':'*'+str(10**63)+'', 'decillion':'*'+str(10**33)+')', 'nonillion':str(10**30)+'', 'octillion':'*'+str(10**27)+'', 'septillion':'*'+str(10**24)+'', 
            'sextillion':'*'+str(10**21)+'', 'quintillion':'*'+str(10**18)+'', 'quadrillion':'*'+str(10**15)+'', 'trillion':'*'+str(10**12)+'', 
            'billion':'*'+str(10**9)+'', 'million':'*'+str(10**6)+'', 'thousand':'*1000', 'hundred':'*100', 
            'eighty':'eightty', 'teen':'+10', 'twelve':'12', 'eleven':'11', 'ten':'10', 
            'nine':'+9', 'eight':'+8', 'seven':'+7', 'six':'+6', 'five':'+5', 'four':'+4', 'three':'+3', 'two':'+2', 'one':'+1', 'zero':'0', 
            'and':'+', 'plus':'+', 'minus':'-', 'negative':'-', 'x':'*', 'times':'*', 'divide':'/', 'point':'.', 'tesseracted':'^4', 'cubed':'^3', 'squared':'^2', 
            'gross':'*144', 'dozen':'*12', 'score':'*20', 'naught':'0', 'none':'0', 'zip':'0', 'nada':'0', 
            'fif':'+5', 'for':'+4', 'thir':'+3', 'twen':'+2', 'ty':'*10', 'π':'pi', '!':'!1', 
            'novem':str(10**27), 'octo':str(10**24), 'septen':str(10**21), 'sex':str(10**18), 'quin':str(10**15), 'quattour':str(10**12), 'tre':str(10**9), 
            'duo':str(10**6), 'un':str(10**3), 'k':'000', 'm':'000000', 
            ')(':')*(',
            '++':'+', '+*':'*', '+/':'/', '+%':'%', '+-':'-', '+^':'^', '*+':'*', '.+':'.', 
            '**':'*', '/*':'/', '%*':'%', '-*':'-', '^*':'^', '<*':'<', '>*':'>',
            '-.':'-0.', '*.':'*0.', '+.':'+0.', '/.':'/0.', '^.':'^0.',
            'ans':self.addprevcalc(uid, '')
            }
        for k, v in rpldic.items():
            s = s.replace(k, v)
        if s.endswith('+'):
            s = s[:-1]
        openp = len(s) - len(s.replace('(', ''))
        closep = len(s) - len(s.replace(')', ''))
        if openp > closep:
            s = s + ')'*(openp-closep)
        elif closep > openp:
            s = '('*(closep-openp) + s
        return s
    
    
    def addprevcalc(self, uid, message):
        file = open('usercalcs.json', 'r+')
        users = json.load(file)
        return (users.get(uid) or "") + message
        
    def storeprevcalc(self, uid, calc):
        file = open('usercalcs.json', 'r+')
        users = json.load(file)
        users.update({uid: calc})
        file = open('usercalcs.json', 'w+')
        file.write(json.dumps(users))
        
    async def dup_char_to_emoji(self, c, dup, emojdup):
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
        if c == 'ab':
            return self.emojdoub[0]
        elif c == 'cl':
            return self.emojdoub[1]
        elif c == 'id':
            return self.emojdoub[2]
        elif c == 'ng':
            return self.emojdoub[3]
        elif c == 'ok':
            return self.emojdoub[4]
        elif c == 'vs':
            return self.emojdoub[5]
        elif c == 'wc':
            return self.emojdoub[6]
        elif c == '!!':
            return self.emojdoub[7]
        elif c == '!?':
            return self.emojdoub[8]
        elif c == 'new':
            return self.emojdoub[9]
        elif c == 'sos':
            return self.emojdoub[10]
        elif c == 'cool':
            return self.emojdoub[11]
        elif c == 'free':
            return self.emojdoub[12]
        elif c == '10':
            return self.emojdoub[13]
            
            
