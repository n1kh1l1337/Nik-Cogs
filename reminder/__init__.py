from .reminder import RemindMe
def setup(bot):
    cog = RemindMe(bot)
    bot.add_cog(cog)
