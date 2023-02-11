import nextcord
from nextcord.ext import commands
from nextcord import Client, Interaction, InteractionMessage, SlashOption, ChannelType, message
from nextcord.abc import GuildChannel
from nextcord.ext import application_checks
import humanfriendly
import cooldowns
choice = {"add":"add","remove":"remove"}

class channelremove(commands.Cog):
  def __init__(self,client):
      self.client = client

  @nextcord.slash_command(name = "channel",guild_ids=[840886992421650452],force_global=True)
  async def channel(self,interaction:Interaction):
    pass

  @channel.subcommand(name = "access",description = "Make a channel visible/invisible to someone.")
  @application_checks.has_permissions(manage_channels=True)
  @application_checks.bot_has_permissions(manage_channels=True)
  @cooldowns.cooldown(1, 10, bucket=cooldowns.SlashBucket.author)
  async def channelaccess(self,interaction:Interaction,user:nextcord.Mentionable=SlashOption(name = "object",description = "The member/role to edit perms of."),type=SlashOption(name = "type",description="Select whether to add or remove perms.",choices=choice),channel:GuildChannel=SlashOption(name = "channel",description = "Channel to remove/add permission.",required=False,channel_types=[ChannelType.text,ChannelType.news])):

    if channel == None:
      channel = interaction.channel

    if not channel.permissions_for(interaction.guild.me).view_channel:
      await interaction.send("I don't have access to that channel\nPermissions needed :\n`view_channel , manage_channels`",ephemeral=True)
      return
    try:
      if user.top_role.position > interaction.guild.me.top_role.position:
        await interaction.send("I can't edit their perms due to role hierarchy!",ephemeral=True)
        return
    except:
      if user.position > interaction.guild.me.top_role.position:
        await interaction.send("I can't edit this role's permissions due to role hierarchy",ephemeral=True)
        return


    if type == "remove":
      overwrite = channel.overwrites_for(user)
      overwrite.send_messages = False
      overwrite.view_channel = False
      overwrite.read_message_history = False
      overwrite.add_reactions = False
      await channel.set_permissions(user,overwrite=overwrite)
      await interaction.send(f"🔒 Removed {user.mention}'s access from {channel.mention}",ephemeral=True)

    if type == "add":

      overwrite = channel.overwrites_for(user)
      overwrite.send_messages = True
      overwrite.view_channel = True
      overwrite.read_message_history = True
      overwrite.add_reactions = True
      await channel.set_permissions(user,overwrite=overwrite)
      await interaction.send(f"🔓 Added {user.mention}'s access to {channel.mention}",ephemeral=True)

  @channel.subcommand(name = "lock",description = "Lock a channel and make it unchatable.")
  @application_checks.has_permissions(manage_channels=True)
  @application_checks.bot_has_permissions(manage_channels=True)
  @cooldowns.cooldown(1, 10, bucket=cooldowns.SlashBucket.author)
  async def lock(self,interaction:Interaction,channel:GuildChannel=SlashOption(name="channel",channel_types=[ChannelType.text,ChannelType.news],description="Choose a channel to lock!",required=False)):

    if channel == None:
      channel = interaction.channel

    if not channel.permissions_for(interaction.guild.me).view_channel:
      await interaction.send("I can't access that channel\nPermissions needed :\n> `view_channel`",ephemeral=True)
      return



    overwrite = channel.overwrites_for(interaction.guild.default_role)

    overwrite.send_messages = False
    await channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
    await interaction.send(f"🔒 {channel.mention} **was locked**.")

  @channel.subcommand(name = "unlock",description = "Unlock a channel and make it chatable.")
  @application_checks.has_permissions(manage_channels=True)
  @application_checks.bot_has_permissions(manage_channels=True)
  @cooldowns.cooldown(1, 10, bucket=cooldowns.SlashBucket.author)
  async def unlock(self,interaction:Interaction,channel:GuildChannel=SlashOption(name="channel",channel_types=[ChannelType.text,ChannelType.news],description="Choose a channel to unlock!",required=False)):

    channel = channel or interaction.channel

    if not channel.permissions_for(interaction.guild.me).view_channel:
      await interaction.send("I can't access that channel\nPermissions needed :\n> `view_channel`",ephemeral=True)
      return

    overwrite = channel.overwrites_for(interaction.guild.default_role)
    overwrite.send_messages = True
    await channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
    await interaction.send(f"🔓 {channel.mention} **was unlocked**.")

  @channel.subcommand(name = "lockdown",description = "Lock all channels in your server.")
  @application_checks.has_permissions(manage_channels=True)
  @application_checks.bot_has_permissions(manage_channels=True)
  @cooldowns.cooldown(1, 10, bucket=cooldowns.SlashBucket.author)
  async def lockdown(self,interaction:Interaction):
    await interaction.response.defer(ephemeral=True)
    unlcha = []
    for channel in interaction.guild.text_channels:
      if not channel.permissions_for(interaction.guild.me).view_channel:
        unlcha.append(channel)
        pass
      else:
        overwrite = channel.overwrites_for(interaction.guild.default_role)
        overwrite.send_messages = True
        await channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
    if len(unlcha) > 0:
      str = ""
      for i in unlcha:
        str+=f"{i.mention} "
      await interaction.followup.send(f"**Successfully disabled all channels but couldn't disable the following channel(s)**\n\n{str}",ephemeral=True)
    if len(unlcha) == 0:
      await interaction.followup.send("**Successfully disabled all channels.**",ephemeral=True)

  @channel.subcommand(name = "slowmode",description = "Set slowmode for a channel.")
  @application_checks.has_permissions(manage_channels=True)
  @application_checks.bot_has_permissions(manage_channels=True)
  @cooldowns.cooldown(1, 10, bucket=cooldowns.SlashBucket.author)
  async def slowmode(self,interaction:Interaction,time:str=SlashOption(name= "time",description = "The time for the slowmode."),channel:GuildChannel=SlashOption(channel_types=[ChannelType.text,ChannelType.news],name = "channel",description = "The channel in which you want to set slowmode.",required=False)):

    if channel == None:
      channel = interaction.channel
    

    if not channel.permissions_for(interaction.guild.me).view_channel:
      await interaction.send("I don't have access to that channel!\nPermissions needed :\n> `view_channel`",ephemeral=True)

    try:
      finalt = humanfriendly.parse_timespan(time)
    except:
      await interaction.send("Invalid time syntax!",ephemeral=True)
      return

    if finalt > 21600:
      await interaction.send("Time can't be bigger than 6hours",ephemeral=True)
      return

    await channel.edit(slowmode_delay = finalt,reason = f"By {interaction.user}")
    await interaction.send(f"Set slowmode for {channel.mention} | {time}")


def setup(client):
  client.add_cog(channelremove(client))