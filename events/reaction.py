import discord
from discord import embeds
from discord.ext import commands

from main import Scrapper, Annonce

from discord.ext.commands import bot

def setup(bot):
    bot.add_cog(Reaction(bot))

class Reaction(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):

        member = payload.member

        if member != self.bot.user:

            channel = self.bot.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            emoji=payload.emoji.name
            embed = message.embeds[0]

            if emoji == "➕":

                annonce = Scrapper.get_this_page(embed.url)

                embed=discord.Embed(title=annonce.title, url=annonce.url, description=annonce.description)
                embed.add_field(name="price", value=str(annonce.price)+" €")
                embed.add_field(name='etat' , value=annonce.etat)
                embed.add_field(name='likes' , value=annonce.likes)
                embed.add_field(name='publier' , value=annonce.publied_at)
                embed.add_field(name='location' , value=annonce.location)
                embed.add_field(name='phone' , value=annonce.phone_number)
                embed.add_field(name='email' , value=annonce.email)
                if len(annonce.images)>0:
                    embed.set_image(url=annonce.images[0])
                await message.edit(embed=embed)

                if member != None:
                    await message.clear_reactions()