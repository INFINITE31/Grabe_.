import nextcord
from nextcord.ext import commands
import urllib
import os
import json
from nextcord import Client, Interaction, SlashOption, ChannelType
from nextcord.abc import GuildChannel
import asyncpraw
from asyncpraw import Reddit
import datetime
import cooldowns


choice = {"r/memes":"r/memes","r/animememes":"r/animememes","r/antijoke":"r/antijoke","r/me_irl":"r/me_irl","r/dankmemes":"r/dankmemes","r/darkmemers":"r/darkmemers","r/F1meme":"r/F1meme"}

Reddit = Reddit(client_id = "client_id" , client_secret = os.getenv('secret') , username = "username" , password = "password" , user_agent = "user_agent")


class memesla(commands.Cog):
  def __init__(self,client):
     self.client = client

  @nextcord.slash_command(name = "meme",description = "Get from a reddit subreddit.")
  @cooldowns.cooldown(1, 10, bucket=cooldowns.SlashBucket.author)
  async def meme_command(self,interaction:Interaction,subreddit=SlashOption(name = "subreddit",description = "The subreddit from which you want the memes",choices = choice)):

    await interaction.response.defer()

    if subreddit == "r/memes":
      sub = "memes"
    if subreddit == "r/animememes":
      sub = "animememes"
    if subreddit == "r/antijoke":
      sub = "antijoke"
    if subreddit == "r/me_irl":
      sub = "me_irl"
    if subreddit == "r/dankmemes":
      sub = "dankmemes"
    if subreddit == "r/darkmemers":
      sub = "darkmemers"
    if subreddit == "r/F1meme":
      sub = "F1meme"

    subreddit = await Reddit.subreddit(display_name=sub)
    while True:
      submission = await subreddit.random()
      if not submission.over_18:
        if submission.url.endswith(".jpg") or submission.url.endswith(".png") or submission.url.endswith(".gif") or submission.url.endswith(".webp"):
          break

    embed = nextcord.Embed(title = submission.title,url=f"https://reddit.com{submission.permalink}",color=nextcord.Colour.random())
    embed.set_image(submission.url)
    embed.set_footer(text=f"By {submission.author.name}")
    embed.timestamp = datetime.datetime.fromtimestamp(submission.created_utc)
    await interaction.followup.send(embed = embed)



def setup(client):
  client.add_cog(memesla(client))


  
