import const
import discord

from datetime import datetime, timedelta
from character import Character, players_online
from disc_instance import get_channel, add_tag, remove_role


async def register(database, author, text):
    canal = get_channel()
    text = text.replace("!cadastrar", "").split(",")
    new = []
    for element in text:
        new.append(element.strip())
    if len(new) != 5:
        await canal.send("Para cadastrar uma ficha, você precisa informar 5 valores"
                         "\nexemplo: !cadastrar Nome, Raca, Classe, Idade, link_foto")
    elif database.consult_player(author.id):
        await canal.send("Você já possui um cadastro registrado")
    else:
        database.create_player(author.id, new[0], new[1], new[2], new[3], new[4])
        players_online[str(author.id)] = {"jogador": Character.load_player(database, author.id)}
        await add_tag(author, "cadastrado")
        await canal.send("Cadastro realizado com sucesso")


async def consult_register(database, author):
    canal = get_channel()
    if database.consult_player(author.id):
        player = database.consult_player(author.id)
        now = datetime.now() + timedelta(hours=const.FUSO)
        color = discord.Color.from_rgb(int(255), int(0), int(0))
        embed = discord.Embed(title="-------  Ficha de personagem  -------",
                              description=f'Level: [{player[6]}] -- '
                                          f'Exp ({player[5]})'
                                          f'\nNome: {player[0]}'
                                          f'\nRaça: {player[1]}'
                                          f'\nClasse: {player[2]}'
                                          f'\nIdade: {player[3]}',
                              color=color,
                              timestamp=now)
        embed.set_thumbnail(url=player[4])
        await canal.send(embed=embed)
    else:
        await canal.send("Voce não possui uma ficha")


async def delete_register(database, author):
    canal = get_channel()
    if database.consult_player(author.id):
        database.delete_player(author.id)
        await remove_role(author, "cadastrado")
        del players_online[str(author.id)]
        await canal.send("Seu cadastro foi deletado")
    else:
        await canal.send("Você não possui uma ficha cadastrada")
