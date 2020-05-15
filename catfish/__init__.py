from .catfish import Catfish

def setup(bot):
   n = Catfish(bot)
   bot.add_cog(n)