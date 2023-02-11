from itertools import cycle
import asyncio
import nextcord
from nextcord.ext import tasks
from nextcord.enums import Status
from nextcord.ext import commands
from nextcord.ext.commands.core import command
from nextcord.utils import get
import json
from pymongo import MongoClient
import dns
import os
import datetime
from datetime import timezone
import itertools
import random
import json
from motorcog import afkdb
from motorcog import reminderdb
from utillity_loadable.giveaway import enterer

cluster = MongoClient(os.getenv("afkdb"))
database = cluster["infinite"]
collection = database["infinite"]

cluster2 = MongoClient(os.getenv("mongo"))
database2 = cluster2["giveaways"]
collection2 = database2["giveaways"]


cluster3 = MongoClient(os.getenv("mongo"))
database3 = cluster3["afks"]
collection3 = database3["afks"]



class idk(commands.Cog):
  def __init__(self , client):
     self.client = client


  @commands.Cog.listener()
  async def on_ready(self):
    self.client.add_view(enterer(self.client))

    cursor = await reminderdb.find({}).to_list(length=None)
    for coll in cursor:
      try:
        user = coll["user"]
        reason = coll["reason"]
        start =  coll["start"]
        end = coll["end"]
        user = self.client.get_user(int(user))
        seconds = (datetime.datetime.fromtimestamp(int(end)) - datetime.datetime.utcnow()).total_seconds()
      except:
        pass
      
      async def sender(user,start,reason):
        await user.send(embed = nextcord.Embed(description=f"Reminder for **{reason}** | **Reminder from** <t:{start}:f>",color=nextcord.Colour.random()))
        await reminderdb.delete_one({"user":user.id,"reason":reason})
        
      try:
        self.client.loop.call_later(seconds,asyncio.create_task,sender(user,start,reason))
      except:
        pass
        

    print(f"{self.client.user} has connected!")

    with open("/assets/open.json","r") as f:
      time = json.load(f)
    date1 = datetime.datetime.utcnow()
    date = date1.strftime("%Y-%m-%d %H:%M:%S.%f")
    time["time"] = f"{date}"

    with open("open.json","w") as f:
      json.dump(time,f,indent = 4)

    await self.client.change_presence(activity = nextcord.Activity(type = nextcord.ActivityType.watching,name = f"{len(self.client.users)} Users | /help")) # changes presence of the bot (status)



  @commands.Cog.listener()
  async def on_message(self,message):
    
    #if message.content.lower() == ("hm"):
      #if not message.channel.name:
        #return
      #await message.channel.send("<:hm:900718609523961887>")
    
    ness = await afkdb.find_one({"user":message.author.id})
    if ness: 
      time = ness["time"]
      await message.reply(f"Welcome back **{message.author.name}** ,I removed your afk , your afk was set <t:{time}:R>")
      collection3.delete_one({"user":message.author.id})

    if len(message.mentions) > 0:
      for member in message.mentions:
        if member != message.author:
          ness = await afkdb.find_one({"user":member.id})
          if ness:
            reason = ness["reason"]
            time = ness["time"]
            if not message.author.bot:
              await message.reply(f"Mentioned user is afk right now | Reason : **{reason}** | <t:{time}:R>")


def setup(client):
  client.add_cog(idk(client))
  


  
