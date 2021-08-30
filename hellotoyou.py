from discord.ext import commands
from dislash import *
import alphazero

# BASE COG AS A TEMPLATE

class mycog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Example of a slash command in a cog
    @slash_commands.command(
    description="Says Hello!",
    guild_ids=alphazero.guilds_ids,
)
    async def hello(self, ctx):
        await ctx.reply("Hello from cog!")


def setup(bot):
    bot.add_cog(mycog(bot))