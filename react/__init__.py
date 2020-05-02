from .react import setup

def setup(bot):
   n = React(bot)
   bot.add_cog(n)