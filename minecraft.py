from discord.ext import commands
from dislash import *
from mojang import MojangAPI
import discord
import alphazero

class minecraftUser(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_commands.command(
    description="Gets info about a Minecraft user.",
    guild_ids=alphazero.guilds_ids,
        options=[
        Option("user", "Specify a Minecraft username.", Type.STRING, required=True),
    ],
)
    async def mcuser(self, ctx):
        uuid = MojangAPI.get_uuid(ctx.get("user"))
        profile = MojangAPI.get_profile(uuid)
        name_history = MojangAPI.get_name_history(uuid)

        name_history = sorted(name_history, key=lambda k: k["changed_to_at"]) 
        name_history_string = ""
        number = 1

        for index in range(len(name_history)):
            for key in name_history[index]:
                if(key == "name"):
                    name_history_string = name_history_string + str(number) + ". " + str(name_history[index][key]) + "\n"
                    number+=1


        embed=discord.Embed(title=profile.name, 
                url=profile.skin_url,
                description = name_history_string,
                color=0x55FF55,
        )
        embed.set_thumbnail(url = "https://crafatar.com/renders/body/" + uuid)
        embed.set_author(name = profile.name, 
                        icon_url = "https://crafatar.com/avatars/" + uuid)
        embed.set_footer(text = "UUID: " + uuid)

        await ctx.reply(embed=embed)




def setup(bot):
    bot.add_cog(minecraftUser(bot))