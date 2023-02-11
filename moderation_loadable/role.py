from code import interact
import nextcord
from nextcord.ext import commands
from nextcord.ext.commands import MissingPermissions
from nextcord.ext.commands import MissingRequiredArgument
from nextcord.ext.commands import BotMissingPermissions
import pymongo
from pymongo import MongoClient
import os
import dns
from nextcord.utils import get
from nextcord import Client, Interaction, InteractionMessage, SlashOption, ChannelType, message
from nextcord.abc import GuildChannel
from nextcord.utils import get
import datetime
from datetime import timezone
from nextcord.ext import application_checks
import cooldowns

choice2 = {"humans":"humans","bots":"bots","all":"all"}
choice1 = {"add":"add","remove":"remove"}


cluster = MongoClient(os.getenv("prefixd"))
database = cluster["prefix"]
collection = database["prefix"]

class role(commands.Cog):
  def __init__(self,client):
     self.client = client


  @nextcord.slash_command(name = "role")
  async def role(self,interaction:Interaction):
    pass

  @role.subcommand(name = "manage",description = "Manage a member's roles.")
  @application_checks.has_permissions(manage_roles=True)
  @application_checks.bot_has_permissions(manage_roles=True)
  @cooldowns.cooldown(1, 10, bucket=cooldowns.SlashBucket.author)
  async def add(self,interaction:Interaction,user:nextcord.Member=SlashOption(name = "member",description="The member to add/remove the role."),role:nextcord.Role=SlashOption(name="role",description = "The role to add/remove."),choice=SlashOption(name="choice",choices={"add":"add","remove":"removed"},description="Add or remove a role.")):

    if role.position > interaction.user.top_role.position:
      if interaction.user == interaction.guild.owner:
        pass
        
      else:
        await interaction.send("This role is above your league",ephemeral=True)
        return

    if role.position > interaction.guild.me.top_role.position:
      await interaction.send("I can't add/remove this role due to role hierarchy!",ephemeral = True)
      return

    if choice == "add":
      await user.add_roles(role)
      await interaction.send(f"<a:_:913392916095963196> {role} was sucessfully added to {user.name}")

    if choice == "removed":
      await user.remove_roles(role)
      await interaction.send(f"<a:_:913392916095963196> {role} was sucessfully removed from {user.name}")


  @role.subcommand(name = "multiple",description = "Add/Remove a role to/from multiple users.")
  @application_checks.has_permissions(manage_roles=True)
  @application_checks.bot_has_permissions(manage_roles=True)
  @cooldowns.cooldown(1, 60, bucket=cooldowns.SlashBucket.author)
  async def roleall_command(self,interaction:Interaction,type=SlashOption(name = "type",description = "Select whether to add or remove the role.",choices = choice1),role:nextcord.Role=SlashOption(name = "role",description = "Select which role to add/remove."),add_type=SlashOption(name = "user_type",description = "Select whether to add/remove the role to/from humans or bots.",choices = choice2)):


    if role.position > interaction.guild.me.top_role.position:
      await interaction.response.send_message("I can't add/remove this role due to role hierarchy!",ephemeral=True)
      return

    await interaction.response.defer()

    def check(type,add_type,interaction,role):
      if type == "add":
        count = 0
        addlist = []
        if add_type == "bots":
          for member in interaction.guild.members:
            if member.bot:
              if not role in member.roles:
                count+=1
                addlist.append(member)
          return [f"Changing role(s) for {count} bots (add)",addlist]
          
        if add_type == "humans":
          for member in interaction.guild.members:
            if not member.bot:
              if not role in member.roles:
                count+=1
                addlist.append(member)
          return [f"Changing role(s) for {count} humans (add)",addlist]

  
        if add_type == "all":
          for member in interaction.guild.members:
            if not role in member.roles:
              count+=1
              addlist.append(member)
          return [f"Changing role(s) for {count} members (add)",addlist]

      if type == "remove":
        count = 0
        removelist = []
        if add_type == "bots":
          for member in interaction.guild.members:
            if member.bot:
              if role in member.roles:
                count+=1
                removelist.append(member)
          return [f"Changing role(s) for {count} bots (remove)",removelist]
          
        if add_type == "humans":
          for member in interaction.guild.members:
            if not member.bot:
              if role in member.roles:
                count+=1
                removelist.append(member)
          return [f"Changing role(s) for {count} humans (remove)",removelist]
  
        if add_type == "all":
          for member in interaction.guild.members:
            if role in member.roles:
              count+=1
              removelist.append(member)
          return [f"Changing role(s) for {count} members (remove)",removelist]

              

    number = check(type,add_type,interaction,role)
    embed = nextcord.Embed(description = f"<a:_:905091332568141874> {number[0]}",color = 0xED4245)
    embed2 = nextcord.Embed(description = f"<a:_:913392916095963196> Changed roles!",color = 0xED4245)
    
    await interaction.followup.send(embed = embed)
    if type == "add":
      for member in number[1]:
        await member.add_roles(role,reason=f"Added by {interaction.user}")


    if type == "remove":
      for member in number[1]:
        await member.remove_roles(role,reason=f"Removed by {interaction.user}")
    await interaction.channel.send(embed=embed2)


    


def setup(client):
  client.add_cog(role(client))