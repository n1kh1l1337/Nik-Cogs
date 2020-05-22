from .guess import Guess
def setup(bot):
    cog = Guess(bot)
    bot.add_cog(cog)