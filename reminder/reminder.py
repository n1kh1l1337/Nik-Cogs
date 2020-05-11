import discord
from redbot.core import commands
import textwrap
from resources import Timer
import pendulum

class HumanTime(commands.Converter):
    def __init__(self, converter: commands.Converter = None, other=False):
        self.other = other
        self.other_converter = converter

    class HumanTimeOutput:
        def __init__(self, time, other=None):
            self.time = time
            self.other = other

    def parse(self, user_input, ctx):
        settings = {
            'TIMEZONE': 'UTC',
            'RETURN_AS_TIMEZONE_AWARE': True,
            'TO_TIMEZONE': 'UTC',
            'PREFER_DATES_FROM': 'future'
        }

        to_be_passed = f"in {user_input}"
        split = to_be_passed.split(" ")
        length = len(split[:7])
        out = None
        used = ""
        for i in range(length, 0, -1):
            used = " ".join(split[:i])
            out = dateparser.parse(used, settings=settings)
            if out is not None:
                break

        if out is None:
            raise commands.BadArgument('Provided time is invalid')

        now = ctx.message.created_at
        return out.replace(tzinfo=now.tzinfo), ''.join(to_be_passed).replace(used, '')

    def time_check(self, time, ctx):
        now = ctx.message.created_at
        if time is None:
            raise commands.BadArgument('Provided time is invalid')
        elif time < now:
            raise commands.BadArgument('Time is in past')

    async def convert(self, ctx, argument):
        time, other = await ctx.bot.loop.run_in_executor(None, functools.partial(self.parse, argument, ctx))
        self.time_check(time, ctx)
        if self.other_converter is not None:
            other = await self.other_converter.convert(ctx, argument)
        return HumanTime.HumanTimeOutput(time, other)


class Reminders(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    async def remind(self,ctx,time_and_text: HumanTime(other=True)):
        """
        Reminds you of something after a certain amount of time.
        The format must be:
            `remind time text`
        `time` should be a relative time like 2h, 1d, etc
        """
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

    @remind.command(name='list', aliases=['get'])
    async def reminders_list(self, ctx):
        """
        Show 10 of your upcoming reminders
        """

        fetched = await self.bot.timers.timers_service.get_where(extras={"author_id": ctx.author.id}, limit=10)
        if len(fetched) == 0:
            return await ctx.send('No currently running reminders')

        embed = discord.Embed(
            title='Upcoming reminders',
            color=ctx.message.author.top_role.colour
        )
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)

        for timer in fetched:
            text = f"{textwrap.shorten(timer.kwargs['text'], width=512)}"
            embed.add_field(
                name=f'ID: {timer.id}, in {(pendulum.instance(timer.expires_at) - pendulum.now()).in_words()}',
                value=text, inline=False
            )

        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_reminder_timer_complete(self, timer):
        channel = self.bot.get_channel(timer.kwargs['channel_id'])
        member = self.bot.get_guild(timer.kwargs['guild_id']).get_member(timer.kwargs['author_id'])
        delta = (pendulum.instance(timer.expires_at) - pendulum.instance(timer.created_at)).in_words()
        await channel.send(f"{member.mention}, {delta} ago:\n{timer.kwargs['text']}")


def setup(bot):
   n = Reminders(bot)
   bot.add_cog(n)

