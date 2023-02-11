import nextcord
from nextcord.ext import commands
from nextcord.ext.commands import MissingPermissions
from nextcord.ext.commands import MissingRequiredArgument
from nextcord.ext.commands import MemberNotFound
import random
from random import choice
import pymongo
from pymongo import MongoClient
import os
from nextcord.utils import get
from nextcord import slash_command , Interaction , SlashOption
from nextcord.ext import application_checks
import datetime
import cooldowns



class kick(commands.Cog):
    def __init__(self , client):
       self.client = client


    @slash_command(name = "kick",description = "Kicks a member from your server.",guild_ids=[989016906071703652],force_global=True)
    @application_checks.has_permissions(kick_members=True)
    @application_checks.bot_has_permissions(kick_members=True)
    @cooldowns.cooldown(1, 10, bucket=cooldowns.SlashBucket.author)
    async def kick2(self,interaction:Interaction,member:nextcord.Member=SlashOption(name = "member",description="The member which will be kicked."),reason=SlashOption(name = "reason",description = "The reason for kicking the member.",required=False)):

      if reason == None:
        reason = f"Kicked by - {interaction.user}"
      if not reason == None:
        reason+=f" | Kicked by - {interaction.user}"


      if member.top_role.position > interaction.user.top_role.position:
        await interaction.send("Your highest role is below that member's highest role.",ephemeral=True)
        return     

      if member.top_role.position > interaction.guild.me.top_role.position:
        await interaction.send("I can't kick them due to role hierarchy.",ephemeral=True)
        return

      else:
        await interaction.response.defer()
        await interaction.guild.kick(member,reason=reason)
        await interaction.followup.send(f"<a:_:913392916095963196> Successfully kicked **{member.name}**")
  
        try:
  
          embedmm = nextcord.Embed(title = "You were kicked",description = f"You were kicked from {interaction.guild}\n> For : **{reason}**",color = 0xED4245)
          await member.send(embed = embedmm)
      
        except:
          pass
  
def setup(client):
  client.add_cog(kick(client))
