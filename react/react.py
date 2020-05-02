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
    emojis = ["k3llyWave","staresoul", "k3llyWatchinYou", "fedoratip", "02sad"]
    if channel is None:
        channel = ctx.message.channel
    if msg_id is None:
        async for message in channel.history(limit=10):
            msg_id = message
    else:
        try:
            msg_id = await channel.get_message(msg_id)
        except:
            await ctx.send("Message ID {} not found in {}".format(msg_id, channel.mention), delete_after=5)
            return
    if ctx.channel.permissions_for(ctx.me).manage_messages:
        await ctx.message.delete()
    if channel.permissions_for(ctx.me).add_reactions:
        for emoji in emojis:
            try:
                await msg_id.add_reaction(emoji)
            except:
                pass
