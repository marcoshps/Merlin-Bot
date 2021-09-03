import datetime
import discord
import const

from PIL import Image
from connection_db import database
from disc_instance import client


def show_set(_id):
    data = database.consult_set(_id)
    helmet_id = data[0]
    armor_id = data[1]
    legs_id = data[2]
    boots_id = data[3]
    shield_id = data[4]
    weapon_id = data[5]

    helmet = 41, 5
    armor = 41, 43
    legs = 41, 80
    boots = 41, 116
    left_hand = 3, 56
    right_hand = 80, 56

    base = Image.open("imgs/sets/base.png")
    background = Image.open("imgs/sets/set.png")
    foreground = Image.open(f"imgs/sets/{helmet_id}.gif").convert("RGBA")
    base.paste(foreground, (0, 0), foreground)
    background.paste(base, helmet, base)

    base = Image.open("imgs/sets/base.png")
    foreground = Image.open(f"imgs/sets/{armor_id}.gif").convert("RGBA")
    base.paste(foreground, (0, 0), foreground)
    background.paste(base, armor, base)

    base = Image.open("imgs/sets/base.png")
    foreground = Image.open(f"imgs/sets/{legs_id}.gif").convert("RGBA")
    base.paste(foreground, (0, 0), foreground)
    background.paste(base, legs, base)

    base = Image.open("imgs/sets/base.png")
    foreground = Image.open(f"imgs/sets/{boots_id}.gif").convert("RGBA")
    base.paste(foreground, (0, 0), foreground)
    background.paste(base, boots, base)

    base = Image.open("imgs/sets/base.png")
    foreground = Image.open(f"imgs/sets/{weapon_id}.gif").convert("RGBA")
    base.paste(foreground, (0, 0), foreground)
    background.paste(base, left_hand, base)

    base = Image.open("imgs/sets/base.png")
    foreground = Image.open(f"imgs/sets/{shield_id}.gif").convert("RGBA")
    base.paste(foreground, (0, 0), foreground)
    background.paste(base, right_hand, base)
    background.save("imgs/set2.png")


async def show_loot(list, data, title, link_img):
    guild = client.get_guild(const.SERVER_ID)
    canal = guild.get_channel(const.ANUNCIO_ID)
    width = len(list) * 32
    base = Image.open("imgs/sets/base.png")
    base = base.resize((width, 32), Image.ANTIALIAS)

    index = 0
    for item in list:
        foreground = Image.open(f"imgs/sets/{item}.gif").convert("RGBA")
        base.paste(foreground, (index * 32, 0), foreground)
        index = index + 1
    base.save("imgs/loot.png")

    msg = ''
    for item in list:
        msg = msg + f'[ {item} ] ' \
                    f'Nome: {data["Itens"][str(item)]["nome"]}, ' \
                    f'Tipo: {data["Itens"][str(item)]["tipo"]}, ' \
                    f'Ataque: {data["Itens"][str(item)]["ataque"]}, ' \
                    f'Defesa: {data["Itens"][str(item)]["defesa"]}\n'

    now = datetime.datetime.now() + datetime.timedelta(hours=const.FUSO)
    color = discord.Color.from_rgb(int(255), int(0), int(0))
    embed = discord.Embed(title=title,
                          description=msg,
                          color=color,
                          timestamp=now)
    embed.set_thumbnail(url=link_img)
    await canal.send(embed=embed)
    await canal.send(file=discord.File("imgs/loot.png"))
