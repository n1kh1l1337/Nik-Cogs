import discord
from discord.ext import commands

import asyncio
import os
import aiohttp
from datetime import datetime
from utils.settings import GREEN_EMBED, ERROR_EMOJI
import utils.checks
from discord.ext.commands.cooldowns import BucketType
@commands.command()
@commands.cooldown(1,2,BucketType.user)
@commands.guild_only()
@commands.check(utils.checks.is_bot)
async def dadjoke(self, ctx):
        """Says a dad joke. 2 second cooldown."""
        try:
            headers = {"Accept": "application/json"}
            async with aiohttp.ClientSession() as session:
                async with session.get('https://icanhazdadjoke.com', headers=headers) as get:
                    resp = await get.json()
                    embed = discord.Embed(color=GREEN_EMBED)
                    embed.title = "A dad joke."
                    embed.description = f"{resp['joke']}"
                    embed.set_footer(text=f"{self.bot.user.name}")
                    embed.timestamp = datetime.utcnow()
                    await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"{e}")
def setup(bot):
    bot.add_cog(dadjoke(bot))
