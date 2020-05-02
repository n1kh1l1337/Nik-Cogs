import discord
from redbot.core import commands

class React(commands.Cog):
    """ractzz"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def react(self, ctx, msg_id: int = None, channel: discord.TextChannel = None):
        """
            react to a message

            msg_id must be the message ID for desited message within the channel
            channel must be the channel where the desired message is defaults to current channel
            if the bot has manage messages permission it will attempt to delete the command
        """
        emojis = ["<:thinkking:602975162618609676>","<:aldythink:646061177377390612>","<:k3llyThinking:631777147064811532>","🤔" ]
        if channel is None:
            channel = ctx.message.channel
        if msg_id is None:
            async for message in channel.history(limit=2):
                msg_id = message
        else:
            msg_id = await channel.fetch_message(msg_id)
        if ctx.channel.permissions_for(ctx.me).manage_messages:
            await ctx.message.delete()
       
        for emoji in emojis:
            await msg_id.add_reaction(emoji)
def setup(bot):
   n = React(bot)
   bot.add_cog(n)