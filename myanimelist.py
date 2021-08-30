from jikanpy import Jikan

import discord
from discord.ext import commands
from dislash import *
import alphazero

jikan = Jikan()

def searchAnime(name):
    search_result = jikan.search('anime', name)
    return (search_result["results"][0])

def searchManga(name):
    search_result = jikan.search('manga', name)
    return (search_result["results"][0])

def searchUserStats(name):
    search_result = jikan.user(username=name, request='profile')
    return search_result

# First three = anime, last three = manga
def searchUserTopThree(name):
    topAnime = jikan.user(username=name, request='animelist', argument="completed")
    topManga = jikan.user(username=name, request='mangalist', argument="completed")

    topAnime = topAnime["anime"]
    newList = sorted(topAnime, key=lambda i: i['score'], reverse=True)

    topManga = topManga["manga"]
    newList2 = sorted(topManga, key=lambda i: i['score'], reverse=True) 

    return newList[:3] + newList2[:3]


class myanime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_commands.command(
    description="Find an anime/manga on MyAnimeList.",
    guild_ids=alphazero.guilds_ids,
    options=[
        Option("item", "Specify any anime/manga.", Type.STRING, required=True),
    ]
)

    async def malfind(self, ctx):
        row = ActionRow(
            Button(
                style=ButtonStyle.blurple,
                label="Anime",
                custom_id="anime"
            ),
            Button(
                style=ButtonStyle.blurple,
                label="Manga",
                custom_id="manga"
            ),
        )

        msg = await ctx.send("What kind of thing are you looking for :grey_question:", components=[row])

        # Here timeout=60 means that the listener will
        # finish working after 60 seconds of inactivity
        on_click = msg.create_click_listener(timeout=30)
        requested_item = ctx.get("item")

        @on_click.not_from_user(ctx.author, cancel_others=True, reset_timeout=False)
        async def on_wrong_user(inter):
            await inter.reply("You're not the one who used the command! Back away fiend! (ง ื▿ ื)ว", ephemeral=True)

        @on_click.matching_id("anime")
        async def on_anime(inter):
            animeTitle = requested_item
            show = searchAnime(animeTitle)
            embed=discord.Embed(
                title=show["title"], 
                url = show["url"],
                description=show["synopsis"], 
                color=0xFF5733
            )
            embed.set_thumbnail(url=show["image_url"])
            if(show["airing"] == False):
                embed.add_field(name="Airing", value=":x:" + "     (ง ื▿ ื)ว")
            else:
                embed.add_field(name="Airing", value=":white_check_mark:" + "     (ง ื▿ ื)ว")
            embed.add_field(name="Score", value=":star: " + str(show["score"]), inline=True)
            embed.add_field(name="Episodes", value=":cinema: " + str(show["episodes"]), inline=True)
            embed.set_footer(text=show["type"])
            await ctx.send(embed=embed)
            await msg.edit(components=[])
        
        @on_click.matching_id("manga")
        async def on_manga(inter):
            mangaTitle = requested_item
            show = searchManga(mangaTitle)
            embed=discord.Embed(
                title=show["title"], 
                url = show["url"],
                description=show["synopsis"], 
                color=0xFF5733
            )
            embed.set_thumbnail(url=show["image_url"])
            if(show["publishing"] == False):
                embed.add_field(name="Publishing", value=":x:" + "     (ง ื▿ ื)ว", inline=False)
            else:
                embed.add_field(name="Publishing", value=":white_check_mark:" + "     (ง ื▿ ื)ว", inline=False)
            embed.add_field(name="Score", value=":star: " + str(show["score"]), inline=True)
            embed.add_field(name="Volumes", value=":blue_book: " + str(show["volumes"]), inline=True)
            embed.add_field(name="Chapters", value=":green_book: " + str(show["chapters"]), inline=True)
            embed.set_footer(text=str(show["type"]))
            await ctx.send(embed=embed)
            await msg.edit(components=[])

        @on_click.timeout
        async def on_timeout():
            await msg.edit(components=[])
    
    
    @slash_commands.command(
    name="maluser",
    description="Find a User's stats on MyAnimeList.",
    options=[
        Option("item", "Specify a user.", Type.STRING, required=True),
    ]
)
    async def maluser(self, ctx):
        row = ActionRow(
            Button(
                style=ButtonStyle.blurple,
                label="Statistics",
                custom_id="stats"
            ),
            Button(
                style=ButtonStyle.blurple,
                label="Favourites",
                custom_id="favourite"
            ),
        )
        msg = await ctx.send("What do you want to know about this person :grey_question:", components=[row])

        # Here timeout=60 means that the listener will
        # finish working after 60 seconds of inactivity
        on_click = msg.create_click_listener(timeout=30)
        requested_item = ctx.get("item")

        @on_click.not_from_user(ctx.author, cancel_others=True, reset_timeout=False)
        async def on_wrong_user(inter):
            await inter.reply("You're not the one who used the command! Back away fiend! (ง ื▿ ื)ว", ephemeral=True)

        @on_click.matching_id("stats")
        async def on_stats(inter):
            userInfo = searchUserStats(requested_item)
            embed=discord.Embed(
                title= userInfo["username"], 
                url = userInfo["url"],
                description = "Joined: " + str(userInfo["joined"])[0:10]
            )

            embed.set_thumbnail(url=userInfo["image_url"])
            embed.set_footer(text="(ง ื▿ ื)ว")
            embed.add_field(
                name="Anime Statistics", 
                value="Mean Score: " + str(userInfo["anime_stats"]["mean_score"]) + "\n" + 
                    "Watching: " + str(userInfo["anime_stats"]["watching"]) + "\n" +
                    "Completed: " + str(userInfo["anime_stats"]["completed"]) + "\n" + 
                    "Plan to Watch: " + str(userInfo["anime_stats"]["plan_to_watch"]) + "\n" +
                    "Episodes Watched: " + str(userInfo["anime_stats"]["episodes_watched"]),
                inline=True
            )

            embed.add_field(
                name="Manga Statistics", 
                value="Mean Score: " + str(userInfo["manga_stats"]["mean_score"]) + "\n" + 
                    "Reading: " + str(userInfo["manga_stats"]["reading"]) + "\n" +
                    "Completed: " + str(userInfo["manga_stats"]["completed"]) + "\n" + 
                    "Plan to Read: " + str(userInfo["manga_stats"]["plan_to_read"]) + "\n" +
                    "Chapters Read: " + str(userInfo["manga_stats"]["chapters_read"]),
                inline=True
            )
            await ctx.send(embed=embed)
            await msg.edit(components=[])

        @on_click.matching_id("favourite")
        async def on_favourite(inter):
            userList = searchUserTopThree(requested_item)
            userInfo = searchUserStats(requested_item)
            embed=discord.Embed(
                title= userInfo["username"], 
                url = userInfo["url"],
            )
            embed.set_thumbnail(url=userInfo["image_url"])
            embed.set_footer(text="(ง ื▿ ื)ว")

            embed.add_field(
                name="Top Anime", 
                value="1. " + userList[0]["title"] + "\n" + 
                    "2. " + userList[1]["title"] + "\n" + 
                    "3. " + userList[2]["title"] + "\n",
                inline=True
            )
            embed.add_field(
                name="Top Manga", 
                value="1. " + userList[3]["title"] + "\n" + 
                    "2. " + userList[4]["title"] + "\n" + 
                    "3. " + userList[5]["title"] + "\n",
                inline=True
            )
            # pprint.pprint(userList)
            await ctx.send(embed=embed)
            await msg.edit(components=[])

        @on_click.timeout
        async def on_timeout():
            await msg.edit(components=[])


def setup(bot):
    bot.add_cog(myanime(bot))