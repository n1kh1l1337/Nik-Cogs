import discord

from redbot.core import commands, checks, Config

class NicknameChannel(commands.Cog):
    """
    Cog for renaming member that send a message in a channel.
    """
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=46896547)

        default_guild = {
            "channel": None,
            "ignore_role": None,
            "active": False
        }
        self.config.register_guild(**default_guild)

    @checks.bot_has_permissions(manage_channels = True, change_nickname = True)
    @checks.admin_or_permissions(manage_channels = True)
    @commands.group()
    async def nicknamechannelset(self, ctx):
        """
        Configure settings for Nickname Channel.
        """

    @nicknamechannelset.command()
    async def channel(self, ctx, *, channel:discord.TextChannel):
        """
        Configure where the bot should listen.
        """
        await self.config.guild(ctx.guild).channel.set(channel.id)
        await ctx.send(f"Done, user that send a message in {channel.name} will be renamed if the cog is activated.")

    @nicknamechannelset.command()
    async def ignorerole(self, ctx, *, role:discord.Role):
        """
        Add a role that will be ignored.

        User that will send message in this channel that have the set role will be not affected by the bot.
        """
        await self.config.guild(ctx.guild).ignore_role.set(role.id)
        await ctx.send(f"The ignored role is now {role.name}.")

    @nicknamechannelset.command()
    async def active(self, ctx, *, active:bool):
        """
        Choose to activate or not NicknameChannel.

        Choose with `True` or `False`.
        """
        if active is True:
            await self.config.guild(ctx.guild).active.set(True)
            verb = "activated"
        else:
            await self.config.guild(ctx.guild).active.set(False)
            verb = "deactivated"
        await ctx.send(f"The Nickname channel has been {verb}.")

    @commands.Cog.listener()
    async def on_message(self, message):
        # Checks
        if message.guild is None:
            return
        if message.author.bot:
            return
        channel = await self.config.guild(message.guild).channel()
        if channel is None:
            return
        if message.channel.id != channel:
            return
        ignored_role = await self.config.guild(message.guild).ignore_role()
        if ignored_role is not None:
            role = message.guild.get_role(int(ignored_role))
            if role is not None:
                if role in message.author.roles:
                    return
        active = await self.config.guild(message.guild).active()
        if active is False or None:
            return

        # If all checks OK:
        user = message.author
        channel = self.bot.get_channel(channel)
        if len(message.content) > 32:
            m = await channel.send("Your message is too long, if I try to nick you with that, Discord won't allow me, try something shorter.")
            return await m.delete(delay=60)
        try:
            await user.edit(nick=message.content, reason="Modified by Nickname Channel.")
            await message.tick()
            try:
                await channel.set_permissions(user, send_messages=False)
            except discord.Forbidden:
                m = await channel.send("I can't edit channel settings, please contact a server admin and tell him to allow me permission to edit channels.")
                return await m.delete(delay=60)
            except discord.HTTPException:
                m = await channel.send(f"Failed to remove send messages permissions to {user.name}.")
                await m.delete(delay=60)
        except discord.Forbidden:
            m = await channel.send("I'm lacking of permissions, contact a server admin to give me necessary permissions.")
            return await m.delete(delay=60)
        except discord.HTTPException:
            m = await channel.send("Cannot change your nickname, try again.")
            return await m.delete(delay=60)

        try:
            await message.delete(delay=10)
        except discord.Forbidden:
            m = await channel.send("Cannot delete your message, contact a server admin and tell him to give me proper permissions.")
            return await m.delete(delay=60)

def setup(bot):
    n = NicknameChannel(bot)
    bot.add_cog(n)
