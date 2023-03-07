import nextcord
from nextcord.ext import commands
from nextcord.ext.commands import MissingPermissions
from nextcord.ext.commands import MissingRequiredArgument
import pymongo
from pymongo import MongoClient
import os
import dns
from nextcord.utils import get
from nextcord import slash_command , Interaction , SlashOption
import datetime
from nextcord.ext import application_checks
import cooldowns


class ban(commands.Cog):
    def __init__(self,client):
        self.client = client

    @slash_command(name = "ban",description = "Ban members in your server.",guild_ids=[840886992421650452],force_global=True)
    @application_checks.has_permissions(ban_members=True)
    @application_checks.bot_has_permissions(ban_members=True)
    @cooldowns.cooldown(1, 10, bucket=cooldowns.SlashBucket.author)
    async def ban(self,interaction:Interaction,member:nextcord.Member=SlashOption(name="member",description = "Select the member which you want to ban."),reason:str=SlashOption(name="reason",description = "The reason why you want to ban this member.",required=False)):

      if member.top_role.position > interaction.user.top_role.position:
        await interaction.send("Your highest role is below that member's highest role.",ephemeral=True)
        return

      if member.top_role.position > interaction.guild.me.top_role.position:
        await interaction.send("I can't ban them due to role hierarchy.",ephemeral=True)
        return

      else:
        await interaction.response.defer()
        await interaction.guild.ban(member,reason=reason)
        await interaction.followup.send(f"<a:_:913392916095963196> Successfully banned **{member.name}**")
  
        try:
  
          embedmm = nextcord.Embed(title = "You were banned",description = f"You were banned in {interaction.guild}\n> For : **{reason}**",color = 0xED4245)
          await member.send(embed = embedmm)
      
        except:
          pass
  
    @slash_command(name = "unban",description = "Unban someone from your server.")
    @application_checks.has_permissions(ban_members=True)
    @application_checks.bot_has_permissions(ban_members=True)
    @cooldowns.cooldown(1, 10, bucket=cooldowns.SlashBucket.author)
    async def unban(self,interaction:Interaction,user=SlashOption(name = "user",description = "Users to unban, if all banned users aren't shown try typing out their names.")):
        await interaction.response.defer(ephemeral=True)
        bans = interaction.guild.bans(limit=None)
        id = user.split("|")
        print(id)
        id = id[1]
        print(id)
        async for member in bans:
            if member.user.id == int(id):
              await interaction.guild.unban(member.user,reason=f"Unbanned by {interaction.user}")
              break
        await interaction.send(f"<a:_:913392916095963196> Successfully unbanned **{member.user.name}**",ephemeral=True)


    @unban.on_autocomplete("user")
    async def unban_list(self, interaction:Interaction,user:str):
      bans = interaction.guild.bans(limit=None)
      st = []
      async for member in bans:
        if user.lower() in member.user.name.lower():
          st.append(f"{member.user.name} | {member.user.id}")

      await interaction.response.send_autocomplete(st[:25])

def setup(client):
    client.add_cog(ban(client))
