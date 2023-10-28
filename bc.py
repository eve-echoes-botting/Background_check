import discord
import requests
import os
from discord.ext import commands
from itertools import zip_longest

class background_check_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def awoxx(self, ctx, *arg, long = False):
        arg = ' '.join(arg)
        try:
            s = ''
            t, nn, ss = getawoxx(arg)
            await ctx.send(f'total kills: {t}')
            for k, v in sorted(nn.items(), reverse = True, key = lambda x: x[1]):
                s += f'{k}: {v}\n'
                if len(s) > 1500:
                    await ctx.send('```\n' + s + '```')
                    s = ''
            await ctx.send('```\n' + s + '```')
            for i in ss:
                await ctx.send(i)
        except Exception as e:
            await ctx.send(str(e))

    @commands.command()
    async def bc(self, ctx, *arg, long = False):
        arg = ' '.join(arg)
        try:
            s = ''
            r = get(arg)
            t = 0
            nn = {}
            for i in r:
                n = i['victim_full_name']
                t += 1
                if n not in nn:
                    nn[n] = 1
                else:
                    nn[n] += 1
            
            s += f'total kills: {t}\n'
            for k, v in sorted(nn.items(), reverse = True, key = lambda x: x[1]):
                s += f'{k}: {v}\n'
                if len(s) > 1500:
                    await ctx.send('```\n' + s + '```')
                    s = ''
            s = '```\n' + s + f'```\nawoxx detected: {getawoxx(arg)[0]}. use `.awoxx {arg}` to fetch awoxx killmails\n'
            corps = {}
            for i in getall(arg):
                kc = i['killer_corp']
                if kc:
                    if kc not in corps:
                        corps[kc] = 1
                    else:
                        corps[kc] += 1
            s += 'appears on kms while in corps:\n'
            for k, v in sorted(corps.items(), reverse = True, key = lambda x: x[1]):
                s += f'  {k}: {v}\n'
            await ctx.send(s)
        except Exception as e:
            await ctx.send(str(e))

async def setup(bot):
    await bot.add_cog(background_check_cog(bot))

def getawoxx(arg):
    t = 0
    nn = {}
    ss = []
    r = get(arg)
    for i in r:
        if (i['killer_corp'] == i['victim_corp']) and (i['victim_corp'] != ''):
            ss.append('\nhttps://echoes.mobi/killboard/view/killmail/' + i['id'] + '\n' +i['image_url'])
            n = i['victim_full_name']
            t += 1
            if n not in nn:
                nn[n] = 1
            else:
                nn[n] += 1
    return t, nn, ss
 
def getall(arg):
    return [*getone(arg, 'killer'), *getone(arg, 'victim')]

def getone(n, t):
    url = f'https://echoes.mobi/api/killmails?page=1&{t}_name={n}&region=Providence'
    txt = requests.get(url).content.decode('utf-8')
    txt = txt.split('\n')
    keys = txt[0].split(',')
    values = [x.split(',') for x in txt[1:]]
    values = txt[1:]
    d = []
    for i in values:
        if len(i) == 0:
            continue
        tmp = {}
        i = i.split(',')
        key = None
        for j in zip_longest(keys,i):
            if j[0] == 'id' and j[1] == '':
                continue
            if j[0] == 'isk' and j[1] == '"':
                key = 'isk'
            kv = j[0]
            if key:
                kv = key
                key = j[0]
            tmp[kv] = j[1]
        d.append(tmp)
    return d

def get(n):
    url = f'https://echoes.mobi/api/killmails?page=1&killer_name={n}&region=Providence'
    txt = requests.get(url).content.decode('utf-8')
    txt = txt.split('\n')
    keys = txt[0].split(',')
    values = [x.split(',') for x in txt[1:]]
    values = txt[1:]
    d = []
    for i in values:
        if len(i) == 0:
            continue
        tmp = {}
        i = i.split(',')
        key = None
        for j in zip_longest(keys,i):
            if j[0] == 'id' and j[1] == '':
                continue
            if j[0] == 'isk' and j[1] == '"':
                key = 'isk'
            kv = j[0]
            if key:
                kv = key
                key = j[0]
            tmp[kv] = j[1]
        d.append(tmp)
    return d

if __name__ == '__main__':
    get('Vexor')
