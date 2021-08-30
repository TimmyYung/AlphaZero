from discord.ext import commands
from dislash import *
import subprocess
import discord
import alphazero

# BASE COG AS A TEMPLATE

class screen(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_commands.command(
    description="Gives details on the computer the bot is running on.",
    guild_ids=alphazero.guilds_ids,
)
    async def screenfetch(self, ctx):
        cmd = ["screenfetch", "-n", "-N", "-w"]
        output = subprocess.Popen( cmd, stdout=subprocess.PIPE ).communicate()[0].decode('utf-8')
        output = output.split(sep='\n')
        temp_stor = ""
        for i in output[1:]:
            temp_stor = temp_stor + i + "\n" 
        

        embed=discord.Embed(title=output[0], 
                url="https://labists.com/products/labists-raspberry-pi-4g-ram-32gb-card?variant=40549058511007", 
                description=temp_stor, 
                color=0xbc1142)
        embed.set_thumbnail(url="https://www.raspberrypi.org/app/uploads/2018/03/RPi-Logo-Reg-SCREEN.png")
        embed.set_footer(text = "(ง ื▿ ื)ว")
        await ctx.reply(embed=embed)

def setup(bot):
    bot.add_cog(screen(bot))