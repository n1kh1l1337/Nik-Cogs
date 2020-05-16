from .hack import Hack
def setup(bot):
    cog = Hack(bot)
    bot.add_cog(cog)