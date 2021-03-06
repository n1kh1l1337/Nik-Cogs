import discord
from redbot.core import commands, checks, Config
import asyncio
import aiohttp
import json
from datetime import datetime
from discord.ext.commands.cooldowns import BucketType

class YoMama(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    @commands.cooldown(1,2,BucketType.user)
    @commands.guild_only()
    async def yomama(self, ctx):
        """Says a Yomama joke. 2 second cooldown."""
        try:
            async with aiohttp.ClientSession() as session:
                 async with session.get("https://api.yomomma.info/") as response:
                    result = await response.json(content_type='text/html')
                    embed = discord.Embed(color=ctx.message.author.top_role.colour)
                    embed.title = "YoMama!"
                    embed.description = f"{result['joke']}"
                    embed.set_footer(text=f"{self.bot.user.name}")
                    embed.timestamp = datetime.utcnow()
                    await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"{e}")
def setup(bot):
   n = YoMama(bot)
   bot.add_cog(n)

                
