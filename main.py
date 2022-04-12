import discord
from discord import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option

client = commands.Bot(command_prefix="g ")
slash = SlashCommand(client, sync_commands=True)

@slash.slash(
    name="daily",
    description="Gets your daily GCoins"
)
async def _daily(ctx:SlashContext):
    await