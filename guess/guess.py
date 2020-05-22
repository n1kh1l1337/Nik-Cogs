import discord
import random
from redbot.core import commands

class Guess(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    async def guess(self,ctx):
        """Guess a number between 1 to 50"""
        embed = discord.Embed(title='Guess a Number', description='Between 1 and 50',colour=0x00ff00)
        await ctx.send(embed=embed)
        count =0
        def check(m):
            return m.content.isdigit()
        guess = await self.bot.wait_for('message', check=check)
        winner=guess.author.mention
        answer = random.randint(1,50)
        while int(guess.content) != answer:
            guess = await self.bot.wait_for('message', check=check)
            count+=1
        embed = discord.Embed(title='Congrats!!',colour=0x00ff00)
        embed.description=':tada: **| Finally someone guessed it right !! Congratulations to our winner :** '
        embed.add_field(name='**Winner : **', value='{}'.format(winner), inline=False)
        embed.add_field(name='**The correct number was : **', value= answer, inline=False)
        embed.add_field(name='**Total tries :**', value= count+1)
        await ctx.send(embed=embed)