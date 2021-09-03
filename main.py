import const
import discord
import image_generator

from monster import Monster
from connection_db import database
from character import Character, players_online
from register import register, consult_register, delete_register
from disc_instance import client, add_tag, add_exhausted, remove_exhausted


@client.event
async def on_member_join(member):
    await add_tag(member, "aguardando aprovação")


# Função para instanciar jogador quando ficar online
# Também utilizado para excluir a instancia quando estiver offline
@client.event
async def on_member_update(before, after):
    if "cadastrado" in str(before.roles):
        if str(before.status) == "offline" and str(after.status) == "online":
            players_online[str(before.id)] = {"jogador": Character.load_player(database, before.id)}
        elif str(before.status) == "online" and str(after.status) == "offline":
            if str(str(before.id)) in players_online:
                del players_online[str(before.id)]


# Função para instanciar os jogadores que estiverem online
# que possuem cadastro, no momento que o bot ficar online
# baseado na role "cadastrado"
@client.event
async def on_ready():
    guild = client.get_guild(const.SERVER_ID)
    for x in guild.members:
        if str(x.status) != "offline" and "cadastrado" in str(x.roles):
            players_online[str(x.id)] = {"jogador": Character.load_player(database, x.id)}
    print("bot online")


# Comandos de chat
@client.event
async def on_message(message):
    guild = client.get_guild(const.SERVER_ID)
    canal = guild.get_channel(const.ANUNCIO_ID)
    member = message.author

    if message.author.id == 878086177863909406:
        pass

    elif message.channel.id in const.BOT_CHANNELS:
        await add_exhausted()

        # Ação jogador: exemplo !cadastrar Nome, Raca, Classe, Idade, link_foto
        if '!cadastrar' in message.content:
            if "verificado" in str(message.author.roles):
                await register(database, message.author, message.content)
            else:
                await canal.send("Solicite a um administrador sua verificação para participar")
            await remove_exhausted()

        if "cadastrado" in str(message.author.roles):
            # Ação jogador: deletar cadastro ( deleta totalmente o cadastro )
            if message.content == "!deletar cadastro":
                await delete_register(database, message.author)
                await remove_exhausted()

            # Ação jogador: visualização da ficha de cadastro
            elif message.content == "!meu cadastro":
                await consult_register(database, message.author)
                await remove_exhausted()

            # Ação jogador: visualizar set atual
            elif message.content == "!meu set":
                image_generator.show_set(member.id)
                await canal.send(file=discord.File("imgs/set2.png"))
                await remove_exhausted()

            # Gerar monstro exemplo: !gerar Demon
            elif "!gerar " in message.content:
                monster_name = message.content.replace("!gerar ", "")
                await Monster.load_monster("Demonios", monster_name)
                await remove_exhausted()

            # Ação jogador: exemplo !atacar Demon
            elif "!atacar" in message.content:
                attacker = message.content.replace("!atacar ", "")
                await players_online[str(message.author.id)]["jogador"].on_attack(attacker)
                await remove_exhausted()

            # Ação jogador: pegar um item baseado em seu ID
            elif "!pegar" in message.content:
                item = message.content.replace("!pegar ", "")
                await players_online[str(message.author.id)]["jogador"].pick_up(item)
                await remove_exhausted()

            # Ação jogador: mostrar a lista de loot disponível para pegar
            elif "!loot disponivel" in message.content:
                await Character.loot_available()
                await remove_exhausted()

            # Ação jogador: mostrar o seu inventario atual
            elif "!meu inventario" in message.content:
                await players_online[str(message.author.id)]["jogador"].my_inventory()
                await remove_exhausted()

            # Ação jogador: equipar um item que está em seu inventário baseado no ID
            elif "!equipar" in message.content:
                item = message.content.replace("!equipar ", "")
                await players_online[str(message.author.id)]["jogador"].update_set(item)
                await remove_exhausted()

            # Ação jogador: verificar status atual
            elif message.content == "!meu status":
                await players_online[str(message.author.id)]["jogador"].player_status()
                await remove_exhausted()
            else:
                await remove_exhausted()
        else:
            await canal.send("Você precisa de um cadastro para utilizar este comando")
            await remove_exhausted()


# MAIN LOOP

client.run(const.BOT_TOKEN)
