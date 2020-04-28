import discord
from redbot.core import commands

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
        'titles': [],
        'similar_images': []
    }

    for div in soup.findAll('div', attrs={'class':'g'}):
        sLink = div.find('a')
        results['links'].append(sLink['href'])

    for desc in soup.findAll('span', attrs={'class':'st'}):
        results['descriptions'].append(desc.get_text())

    for title in soup.findAll('h3', attrs={'class':'r'}):
        results['titles'].append(title.get_text())

    for similar_image in soup.findAll('div', attrs={'rg_meta'}):
        tmp = json.loads(similar_image.get_text())
        img_url = tmp['ou']
        results['similar_images'].append(img_url)

    return json.dumps(results)

class Catfish(commands.Cog):
    """Do a Google Image Search on a user's avatar!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def catfish(self, ctx: commands.Context, author : discord.Member):
        # avatarUrl = user.avatar_url
        # for similarImg in parseResults(doImageSearch(user.avatar_url))[2]:
        #     print(similarImg)

        msgReply = 'Top 3 similar images to ' + author.name + '#' + author.discriminator + '\'s avatar:\n'
       
        res = json.loads(parseResults(doImageSearch(author.avatar_url)))
        # for img in res['similar_images']:
        #     # print('img: ' + img)
        #     msgReply += img + '\n'

        msgReply += '<' + res['similar_images'][0] + '>\n'
        msgReply += '<' + res['similar_images'][1] + '>\n'
        msgReply += '<' + res['similar_images'][2] + '>\n'

        # print(res['similar_images'])

        await ctx.send(msgReply)



def setup(bot):
    bot.add_cog(Catfish(bot))
