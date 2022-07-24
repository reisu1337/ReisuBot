import discord
import os
from dotenv import load_dotenv

load_dotenv()
bot = discord.Bot(debug_guilds=[940230466160713769])

@bot.event
async def on_ready():
    print(f"{bot.user} is somehow alive and kicking")

#Test Command
@bot.slash_command(name="hello", description="Say hello then son")
async def hello(ctx):
    await ctx.respond("Hey!")

bot.run(os.getenv('TOKEN'))