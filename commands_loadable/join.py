import nextcord
from nextcord.ext import commands
from nextcord.utils import get




class join(commands.Cog):
  def __init__(self , client):
     self.client = client


  @commands.Cog.listener()
  async def on_guild_join(self,guild):

    infinite = self.client.get_user(742612257275641876)

    embed = nextcord.Embed(title = "Thanks for adding this bot!",description = "Hello I'm Grabe_.\n> Type **/help** and get all the useful commands.\n\n> Please make sure I have `Administrator` permissions so that, you face no issues while using commands.",color = 0xED4245)
    embed.set_thumbnail(url = self.client.user.avatar.url)
    embed.set_footer(text = "INFINITE_.",icon_url = infinite.avatar.url)

    try:
        joinchannel = guild.system_channel
        await joinchannel.send(embed = embed)
    except:
      try:
        for channel in guild.channels:
          if "general" in channel.lower():
            await channel.send(embed = embed)
      except:
        try:
          await guild.text_channels[0].send(embed = embed)
        except:
          pass


def setup(client):
  client.add_cog(join(client))