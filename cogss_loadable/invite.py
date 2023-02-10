import nextcord
from nextcord.ext import commands
from nextcord.utils import get



class invite(commands.Cog):
  def __init__(self,client):
     self.client = client
  
  @commands.command()
  @commands.bot_has_permissions(embed_links = True)
  @commands.cooldown(4,10,commands.BucketType.user)
  async def invite(self,ctx):

    
    owner = await self.client.fetch_user(742612257275641876)


    embed= nextcord.Embed(title = "Trying to invite ?",description = "[Invite Me](https://discord.com/oauth2/authorize?client_id=919174669721014293&permissions=1642758401279&scope=bot%20applications.commands)\n[Support Server](https://discord.io/Zekrom_)",color = nextcord.Colour.random())
    embed.set_footer(text = f"Grabe_. by {owner.name}",icon_url=owner.display_avatar.url)
    embed.set_thumbnail(url = self.client.user.avatar.url)
    embed.timestamp = ctx.message.created_at
    await ctx.send(embed = embed)


def setup(client):
  client.add_cog(invite(client))