import nextcord
from nextcord.ext import commands
import os
from nextcord.ext.commands import CommandError
from nextcord.ext.application_checks import ApplicationMissingPermissions
from nextcord.ext.application_checks import ApplicationBotMissingPermissions
import datetime
from pymongo import MongoClient
from nextcord import ApplicationError
from motorcog import bandb
import sys
from cooldowns import CallableOnCooldown
from dotenv import load_dotenv
load_dotenv()

class IsBannedInt(ApplicationError):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)


class IsInDmsInt(ApplicationError):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)


intent = nextcord.Intents()
intent.guilds = True
intent.members = True
intent.bans = True
intent.emojis = True
intent.guild_messages = True
intent.message_content = True

# The bot's instance
client = commands.Bot(command_prefix=commands.when_mentioned, intents=intent, case_insensitive=True)
client.remove_command("help")


@client.event
async def on_application_command_error(interaction, error):
    error = getattr(error, "original", error)

    if isinstance(error, CallableOnCooldown):
        await interaction.send(f"You are being **rate-limited!** Retry in `{error.retry_after}` **seconds**.",ephemeral=True)
        return

    if isinstance(error, IsInDmsInt):
        await interaction.send("Commands can't be used in DMs", ephemeral=True)
        return

    if isinstance(error, IsBannedInt):
        banned = await bandb.find_one({"user": interaction.user.id})
        reason = banned["reason"]

        embed = nextcord.Embed(description=f"Uh oh looks like you're suspended !\n**Reason :** {reason}",color=0xED4245)
        embed.set_footer(text="Grabe_. team")
        await interaction.send(embed=embed, ephemeral=True)
        return

    if isinstance(error, ApplicationMissingPermissions):
        await interaction.send("You don't have permissions do that!", ephemeral=True)
        return

    if isinstance(error, ApplicationBotMissingPermissions):
        await interaction.send(
            f"I don't have permissiongs to do that!\nPermissions needed:\n> {error.missing_permissions}",
            ephemeral=True)
        return

    else:
        try:
            await interaction.response.send_message("Looks like an unidentified error - This has been reported!",ephemeral=True)
        except:
            pass
        print(error)

@client.check
def is_banned(ctx):
    # Checks if the author is infinite or not
    if not ctx.author.id == 742612257275641876:
        return False

    else:
        return True


@client.application_command_check
async def is_bunned(interaction: nextcord.Interaction):
    if await bandb.find_one({"user": interaction.user.id}):
        raise IsBannedInt(interaction.user)
        return False
    else:
        return True


@client.application_command_check
def dmint(interaction: nextcord.Interaction):
    if interaction.user.id == 742612257275641876:
        return True
    if str(interaction.channel.type) == "private":
        raise IsInDmsInt(interaction.user)
        return False
    if not str(interaction.channel.type) == "private":
        return True


for folders in os.listdir("./"):
    if folders.endswith("_loadable"):
        sys.path.append(f"./{folders}")
        for file in os.listdir(f"./{folders}"):
            if file.endswith(".py"):
                client.load_extension(f"{folders}.{file[:-3]}")
        print(f"Successfully loaded {folders} and all cogs!")


client.load_extension('onami')
client.run(os.getenv("token"))
