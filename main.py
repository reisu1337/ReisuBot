import os
import discord
from discord import client
from discord.ext import commands
from discord.utils import get

client = commands.Bot(command_prefix="!")


@client.event
async def on_ready():
    print("Bot active")
    activity = discord.Game(name="Was Einstein's theory good? Relatively.", type=3)
    await client.change_presence(activity=activity)
    # channel1 = client.get_channel(818536388567236638)
    # await channel1.send("The bot is now active!")


@client.command()
async def pronouns(ctx, pronouns1):
    user = ctx.message.author
    if "/" in pronouns1:
        if get(ctx.guild.roles, name=pronouns1):
            role = discord.utils.get(user.guild.roles, name=pronouns1)
            await discord.Member.add_roles(user, role)
            await ctx.send("Pronouns added!")
        else:
            await ctx.send("These pronouns haven't been added yet, ask a mod to add them for you!")
    else:
        await ctx.send("Make sure your pronouns are formatted as \"a/b\"!")


# noinspection PyPep8Naming
@client.command()
@commands.has_role("Mod")
async def addPronouns(ctx, pronouns2):
    if get(ctx.guild.roles, name=pronouns2):
        await ctx.send("Pronouns are already available!")
    else:
        await ctx.guild.create_role(name=pronouns2)
        await ctx.send(f"Pronouns \"{pronouns2}\" have been added!")


@client.command()
async def test(ctx):
    await ctx.send("This is a test")


my_secret = os.environ['TOKEN']
client.run(my_secret)

# load_dotenv(".env")
# client.run(os.getenv("TOKEN"))
