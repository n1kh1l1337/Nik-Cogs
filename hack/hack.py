import discord
from redbot.core import commands
import random
import asyncio
class Hack(commands.Cog):
    
    @commands.command(pass_context=True)
    async def hack(self,ctx,member: discord.Member=None):
        """ Hacks the user :^) """
        lastmessage = ["pizza is disgusting", "yes"]
        emails = ['yesdaddy@gmail.com','iwantsumd*ck@gmail.com','daddypleaseintome@gmail.com']
        await ctx.channel.trigger_typing()
        member = member or ctx.author
        msg = await ctx.send(f"[▘] Analyzing **{member.name}** right now...")
        await asyncio.sleep(2)
        await msg.edit(content=f"[▝] Finding {member.name}'s login information...")
        await asyncio.sleep(2)
        await msg.edit(content=f"[▗] Login Informaton found\n**Email:** __{random.choice(emails)}__\n**Password:** __*******__")
        await asyncio.sleep(2)
        await msg.edit(content=f"[▖] Analyizing last message sent...")
        await asyncio.sleep(2)
        await msg.edit(content=f"[▘] **Last Message:** __{random.choice(lastmessage)}__")
        await asyncio.sleep(2)
        await msg.edit(content="[▝] Logged in account..")
        await asyncio.sleep(2)
        await msg.edit(content=f"[▗] Searching for discriminator...")
        await asyncio.sleep(2)
        await msg.edit(content=f"[▖] Giving corona to discriminator... `{member.discriminator}`")
        await asyncio.sleep(2)
        await msg.edit(content=f"[▘] Corona succesfully given.")
        await asyncio.sleep(1)
        await msg.edit(content=f"[▝] Sending {member} to the Gulag...")
        await asyncio.sleep(2)
        await msg.edit(content=f"[▗] {member} has been defeated in the Gulag...")
        await asyncio.sleep(2)
        await msg.edit(content=f"[▖] Finding evidence to report to Discord...")
        await asyncio.sleep(2)
        await msg.edit(content=f"[▘] Efidence found. Reporting {member} to Discord")
        await asyncio.sleep(2)
        await msg.edit(content=f"<a:loading:711181652017020958> {member} has been succesfully reported.. account will be disabled in 4 seconds...")
        await asyncio.sleep(4)
        await msg.edit(content=f"[▗] Account has been disabled.. <a:cravrave:711182081178468412>")
        await asyncio.sleep(2)
        await msg.edit(content=f"[▖] Deleting all noticable proof.")
        await asyncio.sleep(1)
        await msg.edit(content=f"Succesfully hacked `{member.name}`")
        await ctx.send("All evidence cleared. Mission accomplished.")