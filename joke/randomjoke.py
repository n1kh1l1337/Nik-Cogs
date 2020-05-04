import discord
from redbot.core import commands, checks, Config
import asyncio
import aiohttp
import json
from datetime import datetime
from discord.ext.commands.cooldowns import BucketType

class RandomJoke(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    @commands.cooldown(1,2,BucketType.user)
    @commands.guild_only()
    async def joke(self, ctx):
        """Says a random joke. 2 second cooldown."""
        try:
            async with aiohttp.ClientSession() as session:
                 async with session.get("https://official-joke-api.appspot.com/random_joke") as response:
                    result = await response.json(content_type='text/html')
                    embed = discord.Embed(color=ctx.message.author.top_role.colour)
                    embed.title = "Random Joke!"
                    embed.description = f"{result['setup']}\n"
                    embed.description = f"{result['punchline']}"
                    embed.set_footer(text=f"{self.bot.user.name}")
                    embed.timestamp = datetime.utcnow()
                    await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"{e}")
def setup(bot):
   n = RandomJoke(bot)
   bot.add_cog(n)
