
import discord
from discord.ext import commands
import json

from main import Scrapper, Annonce, database

import mysql.connector

def setup(bot):
    bot.add_cog(Notice(bot))

class Notice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def notif(self, ctx, *args):
        if len(args) > 0:
            if "affairespc.com/search" in args[0]:
                database.add_user_search(ctx.author.id, args[0])
                annonces : list[Annonce] = Scrapper.search_by_url(args[0])
                urls_already_viewed=[]
                for annonce in annonces:
                    embed=discord.Embed(title=annonce.title, url=annonce.url)
                    embed.add_field(name="price", value=str(annonce.price))
                    if len(annonce.images)>0:
                        embed.set_image(url=annonce.images[0])
                    reply = await ctx.channel.send(embed=embed)
                    database.add_user_link(ctx.author.id, annonce.url)
                    await reply.add_reaction("➕")
