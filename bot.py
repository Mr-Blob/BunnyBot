import discord
import asyncio
import os
import sys
import traceback
import logging
from discord.ext import commands

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

bot = commands.Bot(command_prefix=commands.when_mentioned_or("//"), pm_help=False)
bot.remove_command("help")

exts = ["REPL", "randomstuff", "Logging"]


@bot.listen()
async def on_ready():
    print("Start")

    for ext in exts:
        print(f"Currently Loading {ext}...", end="")
        try:
            bot.load_extension(ext)
        except Exception:
            print(f"Error in loading {ext}.")
            traceback.print_exc()
        else:
            print("All Loaded.")


@bot.event
async def on_member_join(ctx, member: discord.Member):
    role = discord.utils.get(member.guild.roles, name="Non Bunnies")
    await member.add_roles(role)


@commands.is_owner()
@bot.command()
async def reload(ctx, ext):
    bot.unload_extension(ext)
    bot.load_extension(ext)
    await ctx.send(f"**{ext}** has been reloaded")


@commands.is_owner()
@bot.command()
async def unload(ctx, ext):
    bot.unload_extension(ext)
    await ctx.send(f"**{ext}** has been unloaded")


@commands.is_owner()
@bot.command()
async def load(ctx, ext):
    bot.load_extension(ext)
    await ctx.send(f"**{ext}** has been loaded")


@bot.command()
async def say(ctx, *, X):
    await ctx.message.delete()
    await ctx.send('`' + X + '`')


@bot.command()
async def guides(ctx, sel: str):
    if sel.lower() == "f18":
        await ctx.send("https://www.mudspike.com/chucks-guides-dcs-f-a-18c-hornet/")
    elif sel.lower() == "a10":
        await ctx.send("https://www.mudspike.com/chucks-guides-dcs-a-10c-warthog/")
    elif sel.lower() == "f14":
        await ctx.send("https://www.mudspike.com/chucks-guides-dcs-f-14b-tomcat/")
    else:
        await ctx.send("https://www.mudspike.com/chucks-guides-dcs/")


@bot.command()
async def wiki(ctx, sel: str = None):
        await ctx.send("https://wiki.hoggitworld.com/view/Hoggit_DCS_World_Wiki/")



@bot.command()
async def help(ctx, command: str = None):
    await ctx.message.delete()
    em = discord.Embed(title="Help", colour=1467647)
    em.add_field(name="help", value="Shows this menu", inline=False)
    em.add_field(name="say", value="Says back the message...", inline=False)
    await ctx.send(embed=em)
    

bot.run(os.environ['TOKEN'])