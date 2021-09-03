import const
import discord

from time import sleep
from connection_db import database
from random import randint, choice
from disc_instance import get_channel
from image_generator import show_loot
from datetime import datetime, timedelta
from manipulacao_json import loadJson, binary_to_dict
from monster import Monster, loot_on_floor, monster_activated

players_online = {}


class Character:
    def __init__(self, _id, name, age, breed, kind, level, exp, helmet, armor, legs, boots, shield, weapon, backpack,
                 gold, inventory, health, mana, skill):
        self.id = _id
        self.name = name
        self.age = age
        self.breed = breed
        self.kind = kind
        self.level = level
        self.exp = exp
        self.helmet = helmet
        self.armor = armor
        self.legs = legs
        self.boots = boots
        self.shield = shield
        self.weapon = weapon
        self.backpack = backpack
        self.gold = gold
        self.inventory = inventory
        self.attack = 0
        self.defense = 0
        self.health = health
        self.mana = mana
        self.skill = skill
        Character.get_def_attack(self)

    def get_def_attack(self):
        set = []
        set.append(self.helmet)
        set.append(self.armor)
        set.append(self.legs)
        set.append(self.boots)
        set.append(self.shield)
        set.append(self.weapon)
        defense = 0
        attack = 0
        data = loadJson(const.ITEMS)
        for item in set:
            defense += data["Itens"][str(item)]["defesa"]
            attack += data["Itens"][str(item)]["ataque"]
        self.attack = attack
        self.defense = defense

    @staticmethod
    def load_player(data, _id):
        _id = _id
        player = data.consult_player(_id)
        name = player[0]
        age = player[3]
        breed = player[1]
        kind = player[2]
        level = player[6]
        exp = player[5]
        helmet = player[7]
        armor = player[8]
        legs = player[9]
        boots = player[10]
        shield = player[11]
        weapon = player[12]
        backpack = player[13]
        gold = player[14]
        health = player[16]
        mana = player[17]
        skill = player[18]
        inventory = binary_to_dict(player[15])
        return Character(_id, name, age, breed, kind, level, exp, helmet, armor, legs, boots, shield, weapon, backpack,
                         gold, inventory, health, mana, skill)

    @staticmethod
    async def loot_available():
        canal = get_channel()
        data = loadJson(const.ITEMS)
        loot = loot_on_floor
        title = f'Loot disponível no chão'
        link_img = "https://as2.ftcdn.net/jpg/02/43/28/85/500_F_243288557_GFeppMtpHCBNqErPFGYNQPpfk0Vsy7y5.jpg"

        if len(loot_on_floor) > 0:
            await show_loot(loot, data, title, link_img)
        else:
            await canal.send("Não existe nenhum item disponível")

    async def my_inventory(self):
        canal = get_channel()
        data = loadJson(const.ITEMS)
        loot = self.inventory
        title = f'Inventário do {self.name}'
        link_img = "https://elements-cover-images-0.imgix.net/7e68f19f-bda1-4827-834f-d8aca41ededb?auto=compress&crop=edges&fit=crop&fm=jpeg&h=630&w=1200&s=4a757ef7c5ea02bca6d99188dcd2afcd"
        if len(loot) > 0:
            await show_loot(loot, data, title, link_img)
        else:
            await canal.send("Seu inventário está vazio")

    @staticmethod
    def next_level(level):
        return (((level - 6) * level + 17) * level - 12) / 6 * 100

    async def gain_xp(self, value):
        canal = get_channel()
        current_xp = self.exp + value
        if current_xp >= Character.next_level(self.level + 1):
            self.level += 1
            self.health += self.level * 10 + 185
            self.mana += self.level * 15 + 90
            await canal.send(f'\n:up:  :partying_face: Parabéns, você upou do level {self.level - 1} para {self.level} '
                             f':partying_face: :up:')
        self.exp = current_xp
        database.update_level_player(self.id, self.exp, self.level, self.health, self.mana, self.skill)

    @staticmethod
    def get_attack(attack, skill, level):
        maximum = attack * skill * level * 0.004
        minimum = maximum / 2
        return minimum, maximum

    @staticmethod
    def get_defense():
        print('max = armaduratotal * 0,95, #min = armaduratotal * 0,475 ')

    def spin_dice(self):
        spin = randint(1, 20)
        if spin > 10:
            text = choice(const.WIN_DICE)
            color = discord.Color.from_rgb(int(0), int(255), int(0))
        else:
            text = choice(const.LOSE_DICE)
            color = discord.Color.from_rgb(int(255), int(0), int(0))
        now = datetime.now() + timedelta(hours=const.FUSO)
        embed = discord.Embed(title="-------  Os Dados estão na mesa  -------",
                              description=f'{self.name} girou os dados e o resultado foi: {spin} de 20\n{text}',
                              color=color,
                              timestamp=now)
        embed.set_thumbnail(url="http://pa1.narvii.com/6595/168fba19ab4d1c6e309c13bf128909313d1072bc_00.gif")
        return embed, spin

    async def on_attack(self, name):
        canal = get_channel()
        if name in monster_activated:
            _monster = monster_activated[name]["nome"]
            dice = self.spin_dice()
            await canal.send(embed=dice[0])
            if dice[1] > 10:
                value_attack = Character.get_attack(self.attack, self.skill, self.level)
                damage = randint(round(value_attack[0]), round(value_attack[1]))
                _monster.life = _monster.life - damage
                self.skill += 1
                if _monster.life > 0:
                    msg = f"{self.name} causou {damage} de dano no " \
                          f"{_monster.name} e agora ele está com {_monster.life} de vida"
                    await canal.send(msg)
                    await canal.send(f"Agora é a vez do {_monster.name}, aguarde...")
                    sleep(2)
                    await _monster.on_attack(self)
                else:
                    msg = f"{self.name} deu o golpe final e matou o " \
                          f"{_monster.name}, obtendo {_monster.xp} de experiência"
                    await canal.send(msg)
                    await Monster.on_death(name, self)
            else:
                await _monster.on_attack(self)
        else:
            await canal.send(f'Não existe nenhum monstro com o nome {name} em campo')

    async def pick_up(self, item):
        canal = get_channel()
        try:
            item = int(item)
            if item in loot_on_floor:
                loot_on_floor.remove(item)
                self.inventory.append(item)
                database.update_inventory(self.id, self.inventory)
                await canal.send(f'{self.name} pegou o item {item}')
            else:
                await canal.send(f'Não existe nenhum equipamento disponível com este id')
        except:
            await canal.send('Você precisa informar um ID (apenas numeros)')

    async def update_set(self, item):
        canal = get_channel()
        item = int(item)
        if item in self.inventory:
            item_type = ''
            data = loadJson(const.ITEMS)
            if data["Itens"][str(item)]["tipo"] == "helmet":
                self.inventory.append(self.helmet)
                database.update_inventory(self.id, self.inventory)
                self.helmet = item
                item_type = "helmet"
            elif data["Itens"][str(item)]["tipo"] == "armor":
                self.inventory.append(self.armor)
                self.armor = item
                item_type = "armor"
            elif data["Itens"][str(item)]["tipo"] == "legs":
                self.inventory.append(self.legs)
                self.legs = item
                item_type = "legs"
            elif data["Itens"][str(item)]["tipo"] == "boots":
                self.inventory.append(self.boots)
                self.boots = item
                item_type = "boots"
            elif data["Itens"][str(item)]["tipo"] == "shield":
                self.inventory.append(self.shield)
                self.shield = item
                item_type = "shield"
            elif data["Itens"][str(item)]["tipo"] == "weapon":
                self.inventory.append(self.weapon)
                self.weapon = item
                item_type = "weapon"
            self.inventory.remove(item)
            database.update_inventory(self.id, self.inventory)
            database.update_set(self.id, item_type, item)
            Character.get_def_attack(self)
            await canal.send(f'Item equipado {data["Itens"][str(item)]["nome"]} ')
        else:
            await canal.send("Você não possui este item em seu inventário")

    async def player_status(self):
        canal = get_channel()
        now = datetime.now() + timedelta(hours=const.FUSO)
        color = discord.Color.from_rgb(int(255), int(0), int(0))
        embed = discord.Embed(title="-------  Status  -------",
                              description=f':heart: Vida: [{self.health}] | '
                                          f':blue_heart: Mana: [{self.mana}] '
                                          f'\n:round_pushpin: Level: [{self.level}] -- '
                                          f'Exp ({self.exp})'
                                          f'\n:crossed_swords: Ataque: {self.attack} -- '
                                          f'\n:shield: Defesa: {self.defense}'
                                          f'\n:bar_chart: Habilidade: {self.skill}',
                              color=color,
                              timestamp=now)
        embed.set_thumbnail(url="https://thumbs.dreamstime.com/b/linha-%C3%ADcones-do-jogo-pc-rpg-114114737.jpg")
        await canal.send(embed=embed)
