import discord
import aiohttp
import json
import requests
import asyncio
import random
import os
import datetime as dt
from typing import Union
from discord.ext import commands, tasks
from core.utils.views import Views
from datetime import datetime, timedelta
from pymongo import MongoClient
now = datetime.now
mongo_client = MongoClient("mf put your mongo url here")
db = mongo_client["your db name"]
track_collection = db["track_collection"]
name_collection = db["name_collection"]

class Tags(commands.Cog): # made
    def __init__(self, bot: commands.AutoShardedBot): # by
        self.bot = bot # keron
        self.available_tags = [] #join
        
        self.clean_tags_cache.start() # discord.gg/sup or discord.gg/pictures for more
    @commands.Cog.listener() # follow me for more commands
    async def on_user_update(self, before:discord.User, after:discord.User): # command made by keron :3
        if before.avatar == after.avatar:
            if before.discriminator == "0" and before.name.islower(): # change 0001 to the discrim you want to track , 0 is the new discord tags so
                self.bot.dispatch('available_tag', before)
    
    @commands.Cog.listener()
    async def on_available_tag(self, user:discord.User):
        self.available_tags.insert(0,
            {
                "user": user, # invite lavish https://discord.com/api/oauth2/authorize?client_id=1085249378752659516&permissions=8&scope=bot%20applications.commands
                "time": datetime.now()
            }
        )
        
    @tasks.loop(seconds=1800)
    async def clean_tags_cache(self): # invite lavish https://discord.com/api/oauth2/authorize?client_id=1085249378752659516&permissions=8&scope=bot%20applications.commands
        print("cleaning tag cache")
        now = datetime.now()
        for tag in self.available_tags: # invite lavish https://discord.com/api/oauth2/authorize?client_id=1085249378752659516&permissions=8&scope=bot%20applications.commands
            tag_time = tag["time"]
            difference = now - tag_time
            if difference.seconds > 21600:
                self.available_tags.remove(tag)
    
    @commands.command(name = "tags", description="See available 0001 tags")
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user) 
    async def tags(self, ctx:commands.Context):
        async with ctx.typing():
            available_tags = self.available_tags.copy()
            if available_tags: # invite lavish https://discord.com/api/oauth2/authorize?client_id=1085249378752659516&permissions=8&scope=bot%20applications.commands
                max_tags = 10
                tags = tuple(available_tags[x:x + max_tags]  for x in range(0, len(available_tags), max_tags))
                pages = []

                i = 0
                for group in tags:
                    page = discord.Embed()
                    page.set_author(name=ctx.author.name,icon_url=ctx.author.display_avatar.url)
                    page.color = 0x2f3136 # follow my ig @ clittard
                    page.title = f"recent Usernames With __0001__" # invite lavish :3 https://discord.com/api/oauth2/authorize?client_id=1085249378752659516&permissions=8&scope=bot%20applications.commands
                    page.description = '\n'.join([f"`{idx+1+i}` **-** {x['user']}: {discord.utils.format_dt(x['time'], style='R')}" for idx, x in enumerate(group)])
                    pages.append(page)
                    i += len(group) +1
                
                if len(pages) == 1:
                    await ctx.reply(embed=pages[0], mention_author=False)
                else:
                    paginator = Views.Paginator() # invite lavish https://discord.com/api/oauth2/authorize?client_id=1085249378752659516&permissions=8&scope=bot%20applications.commands
                    await paginator.start(ctx,pages)
            else:
                embed = discord.Embed()
                embed.color = 0x2f3136
                embed.description = "> there are no available __tags__!"
                await ctx.reply(embed=embed, mention_author=False)

async def setup(bot: commands.AutoShardedBot): # invite lavish https://discord.com/api/oauth2/authorize?client_id=1085249378752659516&permissions=8&scope=bot%20applications.commands
    await bot.add_cog(Tags(bot))
