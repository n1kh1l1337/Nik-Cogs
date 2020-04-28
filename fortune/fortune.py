import json
import random
from typing import List, Optional

from redbot.core import commands
from redbot.core.utils.chat_formatting import box
from redbot.core.data_manager import bundled_data_path
from datetime import datetime

from .cows import cowsay

class Moo:
    @classmethod
    async def convert(cls, ctx, arg):
        if arg[:3].lower() == "moo":
            return cls()

        raise commands.BadArgument()


class Fortune(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._data: List[str]
        path = bundled_data_path(self) / "fortunes.json"
        with path.open(mode="r", encoding="utf-8") as fp:
            self._data = json.load(fp)
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
        
    @commands.cooldown(1, 30)
    @commands.command(hidden=True, name="cowsay")
    async def _cowsay(self, ctx: commands.Context, *, what_does_the_cowsay: str = ""):
        """
        Moo.
        """
        if not what_does_the_cowsay:
            await ctx.send_help()
            return

        if len(what_does_the_cowsay) > 1500:
            await ctx.send("Moo.")
            return

        await ctx.send(box(cowsay(what_does_the_cowsay)))
def setup(bot):
   n = Fortune(bot)
   bot.add_cog(n)
