import discord
from redbot.core import commands, checks, Config
from datetime import datetime

class Fortune(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.cooldown(1, 30)
    @commands.command(usage="")
    async def fortune(self, ctx: commands.Context, what_does_the_cowsay: Optional[Moo] = None):
        """
        Get a random fortune message.
        """
        fortune = random.choice(self._data)  # nosec
        if what_does_the_cowsay:
            await ctx.invoke(self._cowsay, what_does_the_cowsay=fortune)
            return
        #await ctx.send(box(fortune))
        embed = discord.Embed(color=ctx.message.author.top_role.colour)
        embed.title = "Fortune."
        embed.description = f"{box(fortune)}"
        embed.set_footer(text=f"{self.bot.user.name}")
        embed.timestamp = datetime.utcnow()
        await ctx.send(embed=embed)
def setup(bot):
   n = Fortune(bot)
   bot.add_cog(n)
