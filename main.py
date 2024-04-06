import discord
import re
import HoYoParse

with open("TOKEN", "r", encoding="utf-8") as f:
    TOKEN = f.read()

lang = "en-us"

client = discord.Client(intents=discord.Intents.all())

@client.event
async def on_ready():
    print('\nlogged in successfully!')
    print(f'current language setting: {lang}')
    print(f'working with {client.user.name} ({client.user.id})\n')

@client.event
async def on_message(message: discord.Message):
    if message.author.id == client.user.id:
        return
    
    if "https://hoyo.link/" in message.content:
        p = r'(https:\/\/hoyo\.link\/[0-9a-zA-Z]{8})'
        urls = re.findall(p, message.content)
        if urls:
            data = []
            for url in urls:
                data, isEmbed = await HoYoParse.parseShortLink(url, lang)
                if not data: return
                if isEmbed:
                    embed = discord.Embed.from_dict(data)
                    await message.reply(embed=embed, mention_author=False)
                else:
                    await message.reply(data, mention_author=False)

    if "https://www.hoyolab.com/" in message.content:
        p = r'(https:\/\/www\.hoyolab\.com\/.+?\/[0-9]+)\??'
        urls = re.findall(p, message.content)
        if urls:
            data = []
            for url in urls:
                data, isEmbed = await HoYoParse.parseLink(url, lang)
                if not data: return
                if isEmbed:
                    embed = discord.Embed.from_dict(data)
                    await message.reply(embed=embed, mention_author=False)
                else:
                    await message.reply(data, mention_author=False)

    if "https://m.hoyolab.com/" in message.content:
        p = r'(https:\/\/m\.hoyolab\.com\/#\/.+?\/[0-9]+)\??'
        urls = re.findall(p, message.content)
        if urls:
            data = []
            for url in urls:
                data, isEmbed = await HoYoParse.parseLink(url, lang)
                if not data: return
                if isEmbed:
                    embed = discord.Embed.from_dict(data)
                    await message.channel.send(embed=embed)
                else:
                    await message.channel.send(data)

client.run(TOKEN)
