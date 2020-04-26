import discord
from discord.ext import commands
from redbot.core import commands, checks, Config
import asyncio
import aiohttp
from datetime import datetime
from discord.ext.commands.cooldowns import BucketType

class DadJoke(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1,5,BucketType.user)
    @commands.guild_only()
    async def random(self, ctx):
        """Chooses a random user. 5 second cooldown."""
        
        user = random.choice(ctx.guild.members)
        test = self.bot.get_user(user.id)
        embed = discord.Embed(color=GREEN_EMBED)
        embed.description = f"User ID: {user.id}\nBot: {user.bot}\nJoined At: {humanize.naturaldate(user.joined_at)}\nStatus: {user.status}\n```{user.activity}```"
        embed.set_footer(text=test)
        embed.set_thumbnail(url=user.avatar_url)
        embed.timestamp = datetime.utcnow()
        await ctx.send(embed=embed)
def setup(bot):
   n = DadJoke(bot)
   bot.add_cog(n)
