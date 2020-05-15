import discord
from redbot.core import commands
<<<<<<< HEAD
from redbot.core import checks
from redbot.core import Config
from redbot.core.data_manager import cog_data_path
from redbot.core.utils.chat_formatting import box
from typing import Optional
from google_images_download import google_images_download
import os, shutil

class Catfish(commands.Cog):
	"""Cog that grabs images from Google."""
	def __init__(self, bot):
		self.bot = bot
		self.config = Config.get_conf(self, identifier=99280384939814912)
		self.config.register_guild(
			blocked_members = []
		)
	@commands.command()
	async def catfish(self, ctx,author: discord.Member):
        avt = str(author.avatar_url)
		blocked_members = await self.config.guild(ctx.guild).blocked_members()
		if ctx.author.id in blocked_members:
			return
		image = google_images_download.googleimagesdownload().download({"url": avt, "limit": 4, "output_directory": str(cog_data_path(self))})
		try:
            for _ in range(len(image[req])):
                await ctx.send(file=discord.File(image[req][i]))
		except:
			embed = discord.Embed(
				description="Error uploading file!",
				color = discord.Color(0).from_rgb(255,0,0)
			)
			await ctx.send(embed=embed)
		folder = cog_data_path(self)
		for the_file in os.listdir(folder):
			file_path = os.path.join(folder, the_file)
			try:
				if os.path.isdir(file_path):
					shutil.rmtree(file_path)
			except:
				raise

	@checks.guildowner()
	@commands.guild_only()
	@commands.group(aliases=["imgset"])
	async def gimageset(self, ctx):
		"""All settings relating to GImage. Settings are saved per guild."""
		pass

	@checks.guildowner()
	@commands.guild_only()
	@gimageset.group(invoke_without_command=True)
	async def block(self, ctx, *, mem : Optional[discord.Member] = None):
		"""Add or remove a person to the blocked list of people not allowed to use GImage."""
		async with self.config.guild(ctx.guild).blocked_members() as blocked_members:
			if mem is None:
				return await ctx.send("Please specify a person to block.")
			if mem.id in blocked_members:
				blocked_members.remove(mem.id)
				await ctx.send(f"{mem.display_name} removed from block list.")
			else:
				blocked_members.append(mem.id)
				await ctx.send(f"{mem.display_name} added to block list.")

	@checks.guildowner()
	@commands.guild_only()
	@block.command()
	async def list(self, ctx):
		"""Displays all people blocked from using GImage."""
		blocked_members = await self.config.guild(ctx.guild).blocked_members()
		list = ""
		for x in range(len(blocked_members)):
			try:
				member = ctx.guild.get_member(blocked_members[x])
				list += f"{member.display_name}\n"
			except:
				list += "<Removed member>\n"
		await ctx.send(box(list))
=======
import argparse
import pycurl
import json
from flask import Flask, url_for, json, request
python3 = False
try:
    from StringIO import StringIO
except ImportError:
    python3 = True
    import io as bytesIOModule
from bs4 import BeautifulSoup
if python3:
    import certifi

SEARCH_URL = 'https://www.google.com/searchbyimage?&image_url='

def doImageSearch(image_url):
    """Perform the image search and return the HTML page response."""

    if python3:
        returned_code = bytesIOModule.BytesIO()
    else:
        returned_code = StringIO()
    full_url = SEARCH_URL + image_url

    conn = pycurl.Curl()
    if python3:
        conn.setopt(conn.CAINFO, certifi.where())
    conn.setopt(conn.URL, str(full_url))
    conn.setopt(conn.FOLLOWLOCATION, 1)
    conn.setopt(conn.USERAGENT, 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11')
    conn.setopt(conn.WRITEFUNCTION, returned_code.write)
    conn.perform()
    conn.close()
    if python3:
        return returned_code.getvalue().decode('UTF-8')
    else:
        return returned_code.getvalue()

def parseResults(code):
    """Parse/Scrape the HTML code for the info we want."""

    soup = BeautifulSoup(code, 'html.parser')

    results = {
        'links': [],
        'descriptions': [],
        'similar_images': []
    }
    

    for div in soup.findAll('div', attrs={'class':'g'}):
        sLink = div.find('a')
        results['links'].append(sLink['href'])
    
    for desc in soup.findAll('span', attrs={'class':'st'}):
        results['descriptions'].append(desc.get_text())

    #for similar_image in soup.find('meta', property="og:image"):
        #tmp = json.loads(similar_image.get_text())
        #results['similar_images'].append(tmp)


    return json.dumps(results)

class Catfish(commands.Cog):
    """Do a Google Image Search on a user's avatar!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def catfish(self, ctx: commands.Context, author : discord.Member= None):
        # avatarUrl = user.avatar_url
        # for similarImg in parseResults(doImageSearch(user.avatar_url))[2]:
        #     print(similarImg)
        await ctx.channel.trigger_typing()
        author = author or ctx.author


        msgReply = 'Top similar images to ' + author.name + '#' + author.discriminator + '\'s avatar:\n'
        await ctx.send(msgReply)
        avt=str(author.avatar_url)
        res = json.loads(parseResults(doImageSearch(avt)))
        count=0
        for img in res['links']:
           count+=1
           await ctx.send(img)
           if count==4:
               break
        #for i in res['similar_images']:
            #await ctx.send(i)
        

       # msgReply += res['links'][0] +'\n'
       # msgReply += res['links'][1] +'\n'
       #msgReply += res['links'][2] +'\n'
       # msgReply += res['descriptions'][0] +'\n'
        
        # print(res['similar_images'])

        #await ctx.send(msgReply)


>>>>>>> 115b38cd296916c6cd9e07138c6aa3dc2263cf1c

