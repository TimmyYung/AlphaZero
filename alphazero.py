from discord.ext import commands
from dislash import *
import os
from dotenv import load_dotenv

bot = commands.Bot(command_prefix="!")
slash = SlashClient(bot)
guilds_ids = [824792581509611560, 876962091330863114]   # Insert ID of your guild here
startup_extensions = ["hellotoyou", "myanimelist", "request", "reddit", "dmPerson", "screenfetch", "minecraft"]
load_dotenv()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}!")

for i in startup_extensions:
    bot.load_extension(i)

if __name__ == "__main__":
    bot.run(os.getenv("DISCORD_TOKEN"))