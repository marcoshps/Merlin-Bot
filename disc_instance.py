import const
import discord

from discord.ext import commands


client = discord.Client()
intents = discord.Intents.all()

client = commands.Bot(command_prefix='_', intents=intents)


async def add_tag(member, tag):
    role = discord.utils.get(member.guild.roles, name=tag)
    await member.add_roles(role)


async def remove_role(member, tag):
    role = discord.utils.get(member.guild.roles, name=tag)
    await member.remove_roles(role)


def get_channel():
    guild = client.get_guild(const.SERVER_ID)
    channel = guild.get_channel(const.ANUNCIO_ID)
    return channel


async def add_exhausted():
    guild = client.get_guild(const.SERVER_ID)
    channel = guild.get_channel(const.ANUNCIO_ID)
    await channel.set_permissions(guild.default_role, send_messages=False)


async def remove_exhausted():
    guild = client.get_guild(const.SERVER_ID)
    channel = guild.get_channel(const.ANUNCIO_ID)
    await channel.set_permissions(guild.default_role, send_messages=True)