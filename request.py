from discord.channel import DMChannel
from discord.ext import commands
from dislash import *
import alphazero

class requestThing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @slash_commands.command(
    description="Request an item to add to the Server",
    guild_ids=alphazero.guilds_ids,
    options=[
        Option("item", "Specify any show/manga", Type.STRING, required=True),
    ],
)

    async def request(self, ctx):
        bot = alphazero.bot
        row = ActionRow(
            Button(
                style=ButtonStyle.blurple,
                label="TV Show",
                custom_id="tv_show"
            ),
            Button(
                style=ButtonStyle.blurple,
                label="Movie",
                custom_id="movie"
            ),
            Button(
                style=ButtonStyle.green,
                label="Manga",
                custom_id="manga"
            ),
            Button(
                style=ButtonStyle.link,
                label="Minecraft",
                url = "https://mineshafter.info/"
            ),
            Button(
                style=ButtonStyle.red,
                label="XXX",
                custom_id="xxx",
                disabled="true"
            )
        )

        msg = await ctx.send("What kind of thing are you requesting :grey_question:", components=[row])

        # Here timeout=60 means that the listener will
        # finish working after 60 seconds of inactivity
        on_click = msg.create_click_listener(timeout=60)
        author = await bot.fetch_user("259058935049355276") # OWNER OF THE BOT'S ID
        requested_item = ctx.get("item")


        @on_click.not_from_user(ctx.author, cancel_others=True, reset_timeout=False)
        async def on_wrong_user(inter):
            await inter.reply("You're not the one requesting! Back away fiend!", ephemeral=True)

        @on_click.matching_id("tv_show")
        async def on_tv_show(inter):
            await DMChannel.send(author, "**" + str(ctx.author) + "** requested **TV Show: " + requested_item + "**")
            await inter.reply("Thanks for using Jellyfin. Will get it on the server ASAP (ง ื▿ ื)ว ", ephemeral=True)
        
        @on_click.matching_id("movie")
        async def on_movie(inter):
            await DMChannel.send(author, "**" + str(ctx.author) + "** requested **Movie: " + requested_item + "**")
            await inter.reply("Thanks for using Jellyfin. Will get it on the server ASAP (ง ื▿ ื)ว ", ephemeral=True)

        @on_click.matching_id("manga")
        async def on_manga(inter):
            await DMChannel.send(author, "**" + str(ctx.author) + "** requested **Manga: " + requested_item + "**")
            await inter.reply("Thanks for using Komga. Will get it on the server ASAP (ง ื▿ ื)ว ", ephemeral=True)

        @on_click.matching_id("xxx")
        async def on_manga(inter):
            await DMChannel.send(author, "**" + str(ctx.author) + "** requested **XXX: " + requested_item + "**")
            await inter.reply("How the hell did you press this button??? I thought I disabled it.")

        @on_click.timeout
        async def on_timeout():
            await msg.edit(components=[])

def setup(bot):
    bot.add_cog(requestThing(bot))