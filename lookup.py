
import discord
from discord.ext import commands
from discord.ext import tasks
from typing import Union
from core.utils.views import Views
from datetime import datetime
from datetime import datetime, timedelta
now = datetime.now
import datetime as dt
import os
import aiohttp
import json
import requests
import asyncio
import random
from pymongo import MongoClient


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
            if before.discriminator == "0001" and before.name.islower(): 
                self.bot.dispatch('available_tag', before)
    
    @commands.Cog.listener()
    async def on_available_tag(self, user:discord.User):
        self.available_tags.insert(0,
            {
                "user": user,
                "time": datetime.now()
            }
        )
        
    @tasks.loop(seconds=1800)
    async def clean_tags_cache(self):
        print("cleaning tag cache")
        now = datetime.now()
        for tag in self.available_tags:
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
            if available_tags:
                max_tags = 10
                tags = tuple(available_tags[x:x + max_tags]  for x in range(0, len(available_tags), max_tags))
                pages = []

                i = 0
                for group in tags:
                    page = discord.Embed()
                    page.set_author(name=ctx.author.name,icon_url=ctx.author.display_avatar.url)
                    page.color = 0x2f3136
                    page.title = f"Recent Usernames With __0001__"
                    page.description = '\n'.join([f"`{idx+1+i}` **-** {x['user']}: {discord.utils.format_dt(x['time'], style='R')}" for idx, x in enumerate(group)])
                    pages.append(page)
                    i += len(group) +1
                
                if len(pages) == 1:
                    await ctx.reply(embed=pages[0], mention_author=False)
                else:
                    paginator = Views.Paginator()
                    await paginator.start(ctx,pages)
            else:
                embed = discord.Embed()
                embed.color = 0x2f3136
                embed.description = "> there are no available __tags__!"
                await ctx.reply(embed=embed, mention_author=False)

async def setup(bot: commands.AutoShardedBot):
    await bot.add_cog(Tags(bot))
