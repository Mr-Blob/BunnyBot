import asyncio

import discord
from discord.ext import commands
from google import google


class Random(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def say(self, ctx, *, X):
        await ctx.message.delete()
        await ctx.send('`' + X + '`')

    @commands.command()
    async def vote(self, ctx, length: int, *, question):
        if length < 1200:
            em = discord.Embed(title='Vote', colour=0xff0000)
            em.add_field(name='Question', value='```{}```'.format(question), inline=False)
            length2 = length * 60
            em.add_field(name='Length', value=length2, inline=False)
            msg = await ctx.send(embed=em)
            re1 = await msg.add_reaction('✅')
            re2 = await msg.add_reaction('❌')
            await asyncio.sleep(length2)
            reactions = (await msg.channel.get_message(msg.id)).reactions
            counts = {}
            for reaction in reactions:
                counts[reaction.emoji] = reaction.count - 1 if reaction.me else reaction.count
            if counts['✅'] > counts['❌']:
                await ctx.send(
                    'And the results are in {}, they have voted, over all, :white_check_mark:'.format(
                        ctx.author.mention))
            elif counts['✅'] < counts['❌']:
                await ctx.send('And the results are in {}, they have voted, over all, :x:'.format(ctx.author.mention))
            elif counts['✅'] == counts['❌']:
                await ctx.send('And the results are in {}, it\' a draw!'.format(ctx.author.mention))
        else:
            await ctx.send('Length over 1 hour')

    @commands.command(aliases=['google'])
    async def g(self, ctx, *, query):
        num_page = 1
        search_results = google.search(query, num_page)
        em = discord.Embed(title='Google Search', colour=0xff0000)
        em.add_field(name=search_results[0].name, value=search_results[0].description)
        em.add_field(name='Link', value=search_results[0].link)
        msg = await ctx.send(embed=em)
        await msg.add_reaction('◀')
        await msg.add_reaction('▶')
        count = 0

        def check(r, m):
            return m == ctx.author and r.emoji in ["▶", "◀"]

        while True:
            try:
                timeoutlen = 10 * 60
                reaction, member = await self.bot.wait_for('reaction_add', check=check, timeout=timeoutlen)
            except asyncio.TimeoutError:
                break

            if reaction.emoji == '▶':
                count = count + 1
                if count > 6:
                    await msg.remove_reaction('▶', ctx.author)
                    count = count - 1

                def limit(count, minimum=0, maximum=6):
                    return max(min(count, maximum), minimum)

                await msg.remove_reaction('▶', ctx.author)
                em.set_field_at(0, name=search_results[count].name, value=search_results[count].description)
                em.set_field_at(1, name='Link', value=search_results[count].link)
                await msg.edit(embed=em)
            if reaction.emoji == '◀':
                count = count - 1
                if count < 0:
                    await msg.remove_reaction('◀', ctx.author)
                    count = count + 1

                def limit(count, minimum=0, maximum=7):
                    return max(min(count, maximum), minimum)

                await msg.remove_reaction('◀', ctx.author)
                em.set_field_at(0, name=search_results[count].name, value=search_results[count].description)
                em.set_field_at(1, name='Link', value=search_results[count].link)
                await msg.edit(embed=em)

    @commands.command()
    async def f(self, ctx):
        people = [ctx.author.name]
        em = discord.Embed()
        em.add_field(name='Press F to pay respects', value=f'{ctx.author} paid their respects.')
        msg = await ctx.send(embed=em)
        await msg.add_reaction('🇫')

        def check(r, m):
            r2 = r.message.id == msg.id
            r = r.emoji == '🇫'
            m3 = m.name not in people
            m2 = m != self.bot.user
            return r and m3 and r2 and m2

        while True:
            try:
                reaction, member = await self.bot.wait_for('reaction_add', check=check, timeout=180)
                people.append(member.name)
                await msg.remove_reaction('🇫', member)
                people2 = ', '.join(people)
                em.set_field_at(0, name='Press F to pay respects', value=f'{people2} paid their respects.')
                await msg.edit(embed=em)
            except asyncio.TimeoutError:
                break


def setup(bot):
    bot.add_cog(Random(bot))