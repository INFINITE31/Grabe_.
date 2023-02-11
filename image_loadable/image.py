import nextcord
from nextcord.ext import commands
from nextcord import slash_command, Interaction as interaction , SlashOption
from aniwrapper import anime
import requests
from PIL import Image,ImageFont,ImageDraw
import random 
import asyncio
from io import BytesIO
import cooldowns

class image(commands.Cog):
    def __init__(self,client):
        self.client = client

    @slash_command(name = "image",description = "Image amplification commands")
    async def image(self,interaction):
        pass

    @image.subcommand(name = "hug",description = "Hug a member through the bot.")
    @cooldowns.cooldown(1, 10, bucket=cooldowns.SlashBucket.author)
    async def hug(self,interaction,member:nextcord.Member=SlashOption(name = "member",description="The person whom you want to hug.")):
        
        if member == interaction.user:
          await interaction.send.send("You can't hug yourself",ephemeral=True)
          return
        
        else:
            url = anime.hug(link=True)
            embed = nextcord.Embed(title = f"{interaction.user.name} hugs {member.name}",color = nextcord.Colour.random())
            embed.set_image(url = url)
            await interaction.send(embed = embed)

    @image.subcommand(name = "kiss",description = "Kiss a member through the bot.")
    @cooldowns.cooldown(1, 10, bucket=cooldowns.SlashBucket.author)
    async def kiss(self,interaction,member:nextcord.Member=SlashOption(name = "member",description="The person whom you want to kiss.")):
        
        if member == interaction.user:
          await interaction.send("You can't kiss yourself",ephemeral=True)
          return
        
        else:
            url = anime.kiss(link=True)

            embed = nextcord.Embed(title = f"{interaction.user.name} kisses {member.name}",color = nextcord.Colour.random())
            embed.set_image(url = url)
            await interaction.send(embed = embed)

    @image.subcommand(name = "pat",description = "Pat a member through the bot.")
    @cooldowns.cooldown(1, 10, bucket=cooldowns.SlashBucket.author)
    async def pat(self,interaction,member:nextcord.Member=SlashOption(name = "member",description="The person whom you want to pat.")):
        
        if member == interaction.user:
          await interaction.send.send("You can't pat yourself",ephemeral=True)
          return
        
        else:
            url = anime.pat(link=True)

            embed = nextcord.Embed(title = f"{interaction.user.name} pats {member.name}",color = nextcord.Colour.random())
            embed.set_image(url = url)
            await interaction.send(embed = embed)


    @image.subcommand(name = "kill",description = "Kill a member through the bot (This is not real).")
    @cooldowns.cooldown(1, 10, bucket=cooldowns.SlashBucket.author)
    async def kill(self,interaction,member:nextcord.Member=SlashOption(name = "member",description="The person whom you want to kill.")):
        
        if member == interaction.user:
          await interaction.send.send("You can't kill yourself",ephemeral=True)
          return
        
        else:
            url = anime.kill(link=True)

            embed = nextcord.Embed(title = f"{interaction.user.name} killed {member.name}",color = nextcord.Colour.random())
            embed.set_image(url = url)
            await interaction.send(embed = embed)


    @image.subcommand(name = "punch",description = "Punch a member through the bot.")
    @cooldowns.cooldown(1, 10, bucket=cooldowns.SlashBucket.author)
    async def punch(self,interaction,member:nextcord.Member=SlashOption(name = "member",description="The person whom you want to punch.")):
        
        if member == interaction.user:
          await interaction.send.send("You can't punch yourself",ephemeral=True)
          return
        
        else:
            Api = requests.get("https://neko-love.xyz/api/v1/punch")
            res = Api.json()
            url = res["url"]
            embed = nextcord.Embed(title = f"{interaction.user.name} punches {member.name}",color = nextcord.Colour.random())
            embed.set_image(url = url)
            await interaction.send(embed = embed)


    @image.subcommand(name = "wanted",description = "Make a wanted poster out of a persons's avatar.")
    @cooldowns.cooldown(1, 30, bucket=cooldowns.SlashBucket.author)
    async def wanted(self,interaction,user:nextcord.Member=SlashOption(name = "member",description="The person whom you want make a poster of.",required=False)):

      await interaction.response.defer()

      if user == None:
        user = interaction.user

      W = 724
      H = 1016

      wanted = Image.open("/assets/wanted.png")

      asset = user.avatar.with_size(4096)

      data = BytesIO(await asset.read())

      pfp = Image.open(data)

      pfp = pfp.resize((550,380))
      try:
        wanted.paste(pfp , (95,240) , pfp)
      except:
        wanted.paste(pfp,(95,240))

      if len(user.name) > 15:
        hm = f"{user.name[:15]}..."
      else:
        hm = user.name

      font = ImageFont.truetype("Crimson-Semibold.ttf",85)
      draw = ImageDraw.Draw(wanted)

      w, h = draw.textsize(hm,font=font)

      draw.text(((W-w)/2,750), hm, font=font,fill="black")
      bounty = random.choice(["5","50","1000","1000000","100000000"])
      draw.text((150,845),f"{bounty}",(0,0,0),font=font)
      wanted.save("profile.png")

      await interaction.followup.send(file = nextcord.File("profile.png"))


    @image.subcommand(name = "hornyjail",description = "Send a person to horny jail.")
    @cooldowns.cooldown(1, 30, bucket=cooldowns.SlashBucket.author)
    async def hjail(self,interaction,member:nextcord.Member=SlashOption(name = "member",description="The person whom you want to send to hornyjail.",required=False)):

      if member == None:
        member = interaction.user

      await interaction.response.defer()

      hjail = Image.open("/assets/jail.jpg")
      asset = member.display_avatar.with_size(128)

      data = BytesIO(await asset.read())
      pfp = Image.open(data)
      pfp = pfp.resize((55,50))
      hjail.paste(pfp , (190,100))

      hjail.save("profile2.jpg")

      await interaction.followup.send(file = nextcord.File("profile2.jpg"))


def setup(client):
  client.add_cog(image(client))
