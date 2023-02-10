import nextcord
from nextcord.ext import commands
import asyncio
from pymongo import MongoClient
import os
import datetime
import random
from utillity_loadable.giveaway import ended
import secrets
from motorcog import gwdb
from motorcog import rolldb

class handler(commands.Cog):
  def __init__(self,client):
      self.client = client

  @commands.Cog.listener()
  async def on_ready(self):

    cursor2 = await gwdb.find({}).to_list(length=None)
    print(cursor2)

    for coll in list(cursor2):

      try:
        dbgl = coll["guild"]
        dbcl = coll["channel"]
        dbhs = coll["hoster"]
        dbms = coll["message"]
        end = coll["end"]
        image = coll["image"]
        winners = coll["winners"]
        participants = coll["participants"]
        descriptions = coll["description"]
        seconds = (datetime.datetime.fromtimestamp(int(end)) - datetime.datetime.utcnow()).total_seconds()

        
      except Exception as e:
        print(e)
        pass

      try:
        fngl = self.client.get_guild(int(dbgl))
        fncl = await fngl.fetch_channel(int(dbcl))
        fnms = await fncl.fetch_message(int(dbms))
        fnhs = await self.client.fetch_user(dbhs)
      except Exception as e:
        await gwdb.delete_one({"guild":int(dbgl),"message":int(dbms)})
        print(e)
        pass

      async def ender(guild,channel,message,hoster,winners,img,participants,descriptions):

        users = participants
        total = len(users)
        winnersl = []
        for i in range(int(winners)):
          try:
            
            u = secrets.choice(users)
            users.pop(users.index(u))
            winnersl.append(u)
            
          except:
            pass
    
        str = ""
        for i in winnersl:
          str+=f"{i} "

        emb = message.embeds[0]


        embed2 = nextcord.Embed(description = f"<:dot:995878727210766467> **Winner(s) :** {str}\n<:dot:995878727210766467> **Hosted by :** {hoster.mention}\n<:dot:995878727210766467> **Participants :** **{total}**",color = nextcord.Colour.random())

        if descriptions == "None":
          pass
        else:
          embed2.add_field(name = "Description",value = descriptions,inline=False)
          
        try:
          embed2.set_thumbnail(url = message.guild.icon.url)
        except:
          pass
        if img.startswith("http"):
          embed2.set_image(url = img)
        if not img.startswith("http"):
          pass
        embed2.set_author(name = emb.author.name,icon_url = "https://cdn.discordapp.com/emojis/995918994680860742.png")   
        embed2.timestamp = datetime.datetime.utcnow()
        embed2.set_footer(text = "Ended")
        await message.edit("<a:_:940165974152331274> **GIVEAWAY ENDED** <a:_:940165974152331274>",embed = embed2)
        
        await gwdb.delete_one({"guild":message.guild.id,"message":message.id})
        async def delete(message):
          try:
            await rolldb.delete_one({"message":message.id})
          except:
            pass

        now = datetime.datetime.utcnow()
        then = datetime.timedelta(seconds=604800)
        new_time = now+then
        await rolldb.insert_one({"guild":message.guild.id,"channel":message.channel.id,"hoster":hoster,"message":message.id,"end":new_time.timestamp(),"image":img,"participants":winners,"description":descriptions})
        self.client.loop.call_later(604800,asyncio.create_task,delete(message))
        
        if len(winnersl) == 0:
          str = "`No one`"
        
        await message.channel.send(f"{str} won the **{emb.author.name}** !")
        
        if len(winnersl) < int(winners):
          if not len(users) == int(winners):
            await message.channel.send("**Number of participants were less than required winners.**")

        await message.edit(view=None)
        await message.edit(view=ended())

      try:
        self.client.loop.call_later(seconds,asyncio.create_task,ender(fngl,fncl,fnms,fnhs,winners,image,participants,descriptions))
      except Exception as e:
        print(e)
        pass


def setup(client):
  client.add_cog(handler(client))