import discord
from discord.ext import commands
from dislash import *
import asyncpraw
import random
import alphazero

import os
from dotenv import load_dotenv
load_dotenv()

reddit = asyncpraw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent="DiscordBot",
)


class redditPost(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_commands.command(
    description="Get a random image from a subreddit.",
    guild_ids=alphazero.guilds_ids,
    options=[
        Option("subreddit", "Specify any subreddit", Type.STRING, required=True),
    ]
)

    async def reddit(self, ctx):
        requested_item = ctx.get("subreddit")
        subreddit = await reddit.subreddit(requested_item)
        meme = random.choice([meme async for meme in subreddit.hot(limit=10)])
        # print(meme.url)
        # print(meme.permalink)

        embed = discord.Embed(title=meme.title, 
                            url = "https://www.reddit.com" + meme.permalink)


        redditAuthor = meme.author
        await redditAuthor.load()
        embed.set_author(name = redditAuthor.name,
                        icon_url = redditAuthor.icon_img)
        embed.set_image(url=meme.url)
        await ctx.reply(type=4, embed=embed)
    
def setup(bot):
    bot.add_cog(redditPost(bot))