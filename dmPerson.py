from discord.ext import commands
from dislash import *
import discord
import alphazero

class sendMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.is_owner()
    @slash_commands.command(
    description="Send anonymous DM to someone. **OWNER ONLY**",
    guild_ids=alphazero.guilds_ids,
    options=[
        Option("user", "Specify a user.", Type.USER, required=True),
        Option("message", "What message would you like to send?", Type.STRING, required=True),
    ]
)
    async def senddm(self, ctx):
        user = await alphazero.bot.fetch_user(ctx.get("user").id) # Get user by ID

        embed=discord.Embed(title="Message from Owner:", 
            description=ctx.get("message"), 
            color=0xFF5733
        )
        embed.set_footer(text = "Any messages sent to the Bot cannot be read. (ง ื▿ ื)ว")
        await user.send(embed=embed)
        await ctx.reply("Sent message. (ง ื▿ ื)ว", ephemeral=True)

def setup(bot):
    bot.add_cog(sendMessage(bot))