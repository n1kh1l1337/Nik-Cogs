from datetime import datetime
import discord
from redbot.core import commands
class Roast(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(aliases=["insult"])
    async def roast(self, ctx, *, member: discord.Member = None):
        """
        Insult that guy
        **Note**: These not meant to be taken seriously
        Args:
            member: The guy to insult
        """
        await ctx.channel.trigger_typing()
        member = member or ctx.author
        async with self.bot.clientSession.get("https://insult.mattbas.org/api/insult.json",
                                              headers={"Accept": "application/json"}) as res:
            if res.status != 200:
                await ctx.send("That lucky bastard... An error occurred."
                               "Mission failed bois, we'll get 'em next time")
                return
            insult = (await res.json(content_type="text/json"))['insult']
            embed = discord.Embed(color=ctx.message.author.top_role.colour)
            embed.title = "Roast"
            embed.description = f"{member.mention}, {insult}"
            embed.set_footer(text=f"{self.bot.user.name}")
            embed.timestamp = datetime.utcnow()
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Roast(bot))