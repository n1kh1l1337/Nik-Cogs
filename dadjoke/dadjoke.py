import discord
from redbot.core import commands, checks, Config
import asyncio
import aiohttp
from datetime import datetime
from discord.ext.commands.cooldowns import BucketType

class DadJoke(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    @commands.cooldown(1,2,BucketType.user)
    @commands.guild_only()
    async def dadjoke(self, ctx):
        """Says a dad joke. 2 second cooldown."""
        try:
            headers = {"Accept": "application/json"}
            async with aiohttp.ClientSession() as session:
                async with session.get('https://icanhazdadjoke.com', headers=headers) as get:
                    resp = await get.json()
                    embed = discord.Embed(color=ctx.message.author.top_role.colour)
                    embed.title = "A dad joke."
                    embed.description = f"{resp['joke']}"
                    embed.set_footer(text=f"{self.bot.user.name}")
                    embed.timestamp = datetime.utcnow()
                    await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"{e}")
def setup(bot):
   n = DadJoke(bot)
   bot.add_cog(n)
