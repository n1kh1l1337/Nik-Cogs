import colorsys
import aiohttp
import discord
from redbot.core import checks
from redbot.core import commands
from redbot.core.utils import chat_formatting as chat



def rgb_to_cmyk(r, g, b):
    rgb_scale = 255
    cmyk_scale = 100
    if (r == 0) and (g == 0) and (b == 0):
        # black
        return 0, 0, 0, cmyk_scale

    # rgb [0,255] -> cmy [0,1]
    c = 1 - r / float(rgb_scale)
    m = 1 - g / float(rgb_scale)
    y = 1 - b / float(rgb_scale)

    # extract out k [0,1]
    min_cmy = min(c, m, y)
    c = c - min_cmy
    m = m - min_cmy
    y = y - min_cmy
    k = min_cmy

    # rescale to the range [0,cmyk_scale]
    return c * cmyk_scale, m * cmyk_scale, y * cmyk_scale, k * cmyk_scale

def bool_emojify(bool_var: bool) -> str:
    return "✅" if bool_var else "❌"

class ColorBaby(commands.Cog):
    

    __version__ = "0.0.1"

    # noinspection PyMissingConstructor
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(loop=self.bot.loop)

    def cog_unload(self):
        self.bot.loop.create_task(self.session.close())
    
    @commands.command(aliases=["HEX", "hex"])
    @checks.bot_has_permissions(embed_links=True)
    async def color(self, ctx, color: discord.Color):
        """Shows some info about provided color"""
        colorrgb = color.to_rgb()
        colorhsv = colorsys.rgb_to_hsv(colorrgb[0], colorrgb[1], colorrgb[2])
        colorhls = colorsys.rgb_to_hls(colorrgb[0], colorrgb[1], colorrgb[2])
        coloryiq = colorsys.rgb_to_yiq(colorrgb[0], colorrgb[1], colorrgb[2])
        colorcmyk = rgb_to_cmyk(colorrgb[0], colorrgb[1], colorrgb[2])
        em = discord.Embed(
            title=str(color),
            description="HEX: {}\n"
            "RGB: {}\n"
            "CMYK: {}\n"
            "HSV: {}\n"
            "HLS: {}\n"
            "YIQ: {}\n"
            "int: {}".format(
                str(color),
                colorrgb,
                colorcmyk,
                colorhsv,
                colorhls,
                coloryiq,
                color.value,
            ),
            url=f"http://www.color-hex.com/color/{str(color)[1:]}",
            colour=color,
            timestamp=ctx.message.created_at,
        )
        em.set_thumbnail(
            url=f"https://api.alexflipnote.dev/color/image/{str(color)[1:]}"
        )
        em.set_image(
            url=f"https://api.alexflipnote.dev/color/image/gradient/{str(color)[1:]}"
        )
        await ctx.send(embed=em)