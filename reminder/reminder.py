import pendulum
import HumanTime
import discord
import time
from redbot.core import commands

class Reminder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    async def remind(self,ctx,time_and_text: HumanTime(other=True)):
        time, text = time_and_text.time, time_and_text.other
        timer = Timer(
            event='reminder',
            created_at=ctx.message.created_at,
            expires_at=time,
            kwargs={
                'author_id': ctx.author.id,
                'guild_id': ctx.guild.id,
                'channel_id': ctx.channel.id,
                'text': text
            }
        )
        await self.bot.timers.create_timer(timer)
        delta = (pendulum.instance(timer.expires_at) - pendulum.instance(ctx.message.created_at)).in_words()
        await ctx.send(f"{ctx.author.display_name} in {delta}:\n{timer.kwargs['text']}")

def setup(bot):
   n = Reminder(bot)
   bot.add_cog(n)

