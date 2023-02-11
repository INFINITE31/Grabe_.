import nextcord
from nextcord.ext import commands
from nextcord.utils import get
from nextcord.ext.commands import MissingPermissions
from nextcord.ext.commands import MissingRequiredArgument
from nextcord.ext.commands import MemberNotFound
import datetime
from nextcord import Client, Interaction, InteractionMessage, SlashOption, ChannelType, message
from nextcord.abc import GuildChannel
import humanfriendly
import pymongo
from pymongo import MongoClient
import os
from nextcord.utils import get
from nextcord.ext import application_checks
import cooldowns


cluster = MongoClient(os.getenv("prefixd"))
database = cluster["prefix"]
collection = database["prefix"]




class mute(commands.Cog):
  def __init__(self,client):
     self.client = client

  @nextcord.slash_command(name = "timeout",guild_ids=[840886992421650452],force_global=True)
  async def timeout(self,ineteraction:Interaction):
    pass

  @timeout.subcommand(name = "add",description="Timeout a member in your server.")
  @application_checks.has_permissions(moderate_members=True)
  @application_checks.bot_has_permissions(moderate_members=True)
  @cooldowns.cooldown(1, 10, bucket=cooldowns.SlashBucket.author)
  async def add(self,interaction:Interaction,user:nextcord.Member=SlashOption(name="member",description="The member to add the timeout on."),time:str=SlashOption(name="ends_after",description = "The time after which the timeout will end.",required=False),reason:str=SlashOption(name = "reason",description="The reason for timeout.",required = False)):


      if user.top_role > interaction.guild.me.top_role:
        await interaction.send("I cannot mute them due to role hierarchy!",ephemeral=True)
        return

      if time == None:
    
        await user.edit(timeout = nextcord.utils.utcnow()+datetime.timedelta(seconds=300))

        await interaction.send(f"<a:_:913392916095963196> {user.mention} was sucessfully muted!")

        try:

          collec = collection.find_one({"Guild":interaction.guild.id})
          channel = collec["Channel"]
          fc = await interaction.guild.fetch_channel(int(channel))

          embed = nextcord.Embed(title = "Member muted",description = f"> **{user}** Was Muted\n> By **{interaction.user}**\n> Reason **{reason}**",color = nextcord.Colour.blurple())
          embed.set_thumbnail(url = interaction.guild.icon.url)
          embed.timestamp = datetime.datetime.utcnow()
          await fc.send(embed = embed)

        except:
          pass
    
        try:

          embedmm = nextcord.Embed(title = "You were muted",description = f"You were muted in {interaction.guild}\n> For : **{reason}**\n> Time : {time}",color = 0xED4245)
          await user.send(embed = embedmm)
      
        except:
          pass


      if time:

        try:
          
          time1 = humanfriendly.parse_timespan(time)

        except:

          await interaction.send("Invalid time syntax.",ephemeral=True)
          return

        if time1 > 604800:
          await interaction.send("Can't timeout a user for more than 1 week.",ephemeral=True)
          return
    
        await user.edit(timeout = nextcord.utils.utcnow()+datetime.timedelta(seconds=time1),reason=reason)

        await interaction.send(f"<a:_:913392916095963196> {user.mention} was sucessfully muted!")

        try:

          embedmm = nextcord.Embed(title = "You were muted",description = f"You were muted in {interaction.guild}\n> For : **{reason}**\n> Time : {time}",color = 0xED4245)
          await user.send(embed = embedmm)
      
        except:
          pass


  @timeout.subcommand(name = "remove",description = "Remove timeout from a member.")
  @nextcord.ext.application_checks.has_permissions(moderate_members=True)
  @nextcord.ext.application_checks.bot_has_permissions(moderate_members=True)
  @cooldowns.cooldown(1, 10, bucket=cooldowns.SlashBucket.author)
  async def untimeout_command(self,interaction:Interaction,user:nextcord.Member=SlashOption(name = "member",description="The member to remove timeout from.")):


    if user.top_role > interaction.guild.me.top_role:
      await interaction.send("I cannot mute them due to role hierarchy!",ephemeral=True)
      return

    else:

      await user.edit(timeout = None)

      await interaction.send(f"<a:_:913392916095963196> {user.mention} was sucessfully unmuted!")

      try:

        embedmm = nextcord.Embed(title = "You were muted",description = f"You are now unmuted in {interaction.guild}",color = 0xED4245)
        await user.send(embed = embedmm)
        
      except:
        pass

  
def setup(client):
  client.add_cog(mute(client))
