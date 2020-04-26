import discord
import aiohttp
from datetime import datetime
from redbot.core import commands, checks, Config
@commands.command()
async def dadjoke(self, ctx):
        try:
            headers = {"Accept": "application/json"}
            async with aiohttp.ClientSession() as session:
                async with session.get('https://icanhazdadjoke.com/', headers=headers) as get:
                    resp = await get.json()
                    embed = discord.Embed(color=ctx.message.author.top_role.colour)
                    embed.title = "A dad joke."
                    embed.description = f"{resp['joke']}"
                    embed.set_footer(text=f"{bot.user.name}")
                    embed.timestamp = datetime.utcnow()
                    await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"{e}")
def setup(bot):
    n = dadjoke(bot)
    bot.add_cog(n)
