from discord import channel, client, guild
from dotenv import load_dotenv
import os
import discord
from discord.ext import commands
from discord.utils import get

client = commands.Bot(command_prefix="!")

@client.event
async def on_ready():
    print("Bot active")
    activity = discord.Game(name="Was Einstein's theory good? Relatively.", type=3)
    await client.change_presence(activity=activity)
    #channel1 = client.get_channel(818536388567236638)
    #await channel1.send("The bot is now active!")


@client.command()
async def pronouns(ctx, pronouns):
    message = ctx.message.content
    splitMessage = message.split(" ")
    user = ctx.message.author
    if "/" in pronouns:
        if get(ctx.guild.roles, name=pronouns):
            role = discord.utils.get(user.guild.roles, name=pronouns)
            await discord.Member.add_roles(user, role)
            await ctx.send("Pronouns added!")
        else:
            await ctx.send("These pronouns haven't been added yet, ask a mod to add them for you!")
    else:
        await ctx.send("Make sure your pronouns are formatted as \"a/b\"!")

@client.command()
@commands.has_role("Mod")
async def addPronouns(ctx, pronouns):
    if get(ctx.guild.roles, name=pronouns):
        await ctx.send("Pronouns are already available!")
    else:
        await ctx.guild.create_role(name=pronouns)
        await ctx.send(f"Pronouns \"{pronouns}\" have been added!")

@client.command()
async def test(ctx):
    await ctx.send("This is a test")




load_dotenv(".env")
client.run(os.getenv("TOKEN"))