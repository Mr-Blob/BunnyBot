import asyncio
import os

import discord
from discord.ext import commands


class Logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    async def on_message_delete(message):
        em = discord.Embed(title='Message Deleted', colour=0x0000ff)
        em.add_field(name='Member:', value=message.author, inline=False)
        em.add_field(name='Message', value=message.content, inline=False)
        channel = discord.utils.get(message.guild.channels, name='logs')
        await channel.send(embed=em)

    async def on_message_edit(before, after):
        em = discord.Embed(title='Message Edit')
        em.add_field(name='Member:', value=before.author, inline=False)
        em.add_field(name='Before:', value=before, inline=False)
        em.add_field(name='After:', value=after, inline=False)
        channel = discord.utils.get(before.guild.channels, name='logs')
        await channel.send(embed=em)


def setup(bot):
    bot.add_cog(Logging(bot))