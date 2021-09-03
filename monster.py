import const
import discord

from time import sleep
from random import choice, randint
from image_generator import show_loot
from manipulacao_json import loadJson
from datetime import datetime, timedelta
from disc_instance import get_channel, client, add_tag


monster_activated = {}
loot_on_floor = []


class Monster:
    def __init__(self, name, life, xp, strength, level, img, loot, body, says):
        self.name = name
        self.life = life
        self.xp = xp
        self.strength = strength
        self.level = level
        self.img = img
        self.loot = loot
        self.body = body
        self.says = says

    @staticmethod
    async def load_monster(kind, name):
        canal = get_channel()
        if name in monster_activated:
            await canal.send(f'Já existe um {name} ativo no cenário')
        else:
            data = loadJson(const.MONSTER)
            if name in data[kind]:
                name = data[kind][name]["nome"]
                life = data[kind][name]["vida"]
                xp = data[kind][name]["xp"]
                strength = data[kind][name]["max_hit"]
                level = data[kind][name]["level"]
                img = data[kind][name]["foto"]
                loot = data[kind][name]["loot"]
                body = data[kind][name]["corpose"]
                says = data[kind][name]["says"]
                monster_activated[name] = {"nome": Monster(name, life, xp, strength, level, img, loot, body, says)}
                now = datetime.now() + timedelta(hours=const.FUSO)
                color = discord.Color.from_rgb(int(255), int(0), int(0))
                embed = discord.Embed(title="-------  Respawn  -------",
                                      description=f'um monstro acabou de nascer!!!\n'
                                                  f'{monster_activated[name]["nome"].name} - '
                                                  f'[{monster_activated[name]["nome"].level}]\n'
                                                  f'vida: {monster_activated[name]["nome"].life}\n'
                                                  f'exp: {monster_activated[name]["nome"].xp}\n',
                                      color=color,
                                      timestamp=now)
                embed.set_thumbnail(url=monster_activated[name]["nome"].img)
                await canal.send(embed=embed)
            else:
                await canal.send(f"Não existe nenhum monstro cadastro com o nome {name}")

    @classmethod
    def get_attack(cls, strength, level_mob, level_player):
        diff = level_mob - level_player
        maximum = strength
        if diff > 0:
            maximum = strength * diff / 2
        minimum = maximum / 2
        return minimum, maximum

    async def on_attack(self, attacker):
        guild = client.get_guild(const.SERVER_ID)
        canal = get_channel()
        await canal.send(f"{self.name}: *{choice(self.says)}*")
        sleep(2)
        value_attack = Monster.get_attack(self.strength, self.level, attacker.level)
        damage = randint(round(value_attack[0]), round(value_attack[1]))
        attacker.health = attacker.health - damage
        if attacker.health > 0:
            await canal.send(f'{attacker.name} recebeu um ataque de {damage} do {self.name} '
                             f'e ficou com {attacker.health} de vida')
        else:
            await canal.send(f'{attacker.name} recebeu um ataque devastador e foi mandado direto para enfermaria\n'
                             f'precisará aguardar sua recuperação para voltar ao combate')
            member = guild.get_member(attacker.id)
            await add_tag(member, "em recuperação")

    @classmethod
    async def on_death(cls, monster_name, killer):
        mob = monster_activated[monster_name]["nome"]
        await killer.gain_xp(mob.xp)
        await Monster.drop_loot(mob.loot, mob.name, mob.body)
        del monster_activated[monster_name]

    @classmethod
    async def drop_loot(cls, loot, mob_name, mob_body):
        for item in loot:
            loot_on_floor.append(item)
        data = loadJson(const.ITEMS)
        title = f'Dead {mob_name}'
        await show_loot(loot, data, title, mob_body)
