
import discord
from discord.ext import commands

from scrapper import Scrapper, Annonce

def setup(bot):
    bot.add_cog(Get(bot))

class Get(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def get(self, ctx, *args):
        if len(args) > 0:
            if "affairespc.com/search" in args[0]:
                annonces : list[Annonce] = Scrapper.search_by_url(args[0])
                for annonce in annonces:
                    embed=discord.Embed(title=annonce.title, url=annonce.url)
                    embed.add_field(name="price", value=str(annonce.price)+ "€")
                    if len(annonce.images)>0:
                        embed.set_image(url=annonce.images[0])
                    reply = await ctx.channel.send(embed=embed)
                    await reply.add_reaction("➕")
                await ctx.message.delete()