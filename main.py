import discord
from discord.ext import commands
from discord.utils import get

import asyncio
import os
import mysql.connector
import json

from scrapper import Scrapper, Annonce
from database import Database

config_file=json.load(open("./config.json"))
prefix = config_file["prefix"]
token = config_file["token"]

config_database=config_file["database"]
ip = config_database["ip"]
port = config_database["port"]
user = config_database["user"]
password = config_database["password"]
database = config_database["database"]

database = Database(ip, port, user, password, database)

intents = discord.Intents().all()
bot=commands.Bot(command_prefix=prefix, description="Bot affaire pc", intents=intents)

@bot.command()
async def load(ctx, name=None):
    if name:
        bot.load_extension(name)
        print(name, "has been loaded")
        await ctx.send(str(name + " has been loaded"))
    
@bot.command()
async def unload(ctx, name=None):
    if name:
        bot.unload_extension(name)
        print(name, "has been unloaded")
        await ctx.send(str(name + " has been unloaded"))

@bot.command()
async def reload(ctx, name=None):
    if name:
        try:
            bot.reload_extension(name)
            print(name, "has been reloaded")
            await ctx.send(str(name + " has been reloaded"))
        except:
            bot.load_extension(name)
            print(name, "has been loaded")
            await ctx.send(str(name + " has been loaded"))

for folder in ["commands", "events"]:
    for file in os.listdir("./{}".format(folder)):
        if file.endswith(".py"):
            bot.load_extension('{}.{}'.format(folder, file[:-3]))
            print(file, "has been loaded")

async def scan():
    await bot.wait_until_ready()
    print("bot started")
    while True:
        for search in database.get_all_searchs():
            annonces = Scrapper.search_by_url(search)
            for user in database.get_users_by_search(search):
                print(type(user))
                links_of_this_user = database.get_user_links(user)
                for annonce in annonces:
                    print(links_of_this_user)
                    if not annonce.url in links_of_this_user:
                        embed=discord.Embed(title=annonce.title, url=annonce.url)
                        embed.add_field(name="price", value=str(annonce.price))
                        if len(annonce.images)>0:
                            embed.set_image(url=annonce.images[0])

                        message = await bot.get_user(user).send(embed=embed)
                        await message.add_reaction("➕")  
                        database.add_user_link(user, annonce.url)
            print(search)             
            await asyncio.sleep(10)

bot.loop.create_task(scan())
bot.run(token)