from discord import channel, client, guild
from dotenv import load_dotenv
import os
import json
import discord
import requests
from twitchAPI.twitch import Twitch
from discord.ext import commands, tasks
from discord.utils import get

intents = discord.Intents.all()
client = commands.Bot(command_prefix="!", intents=intents)

#twitch auth
client_id = os.environ['CLIENT_ID']
client_secret = os.environ['CLIENT_SECRET']
twitch = Twitch(client_id, client_secret)
twitch.authenticate_app([])
TWITCH_STREAM_API_ENDPOINT_V5 = "https://api.twitch.tv/kraken/streams/{}"
API_HEADERS = {
    'Client-ID': client_id,
    'Accept': 'application/vnd.twitchtv.v5+json',
}



@client.event
async def on_ready():
    print("Bot active")
    activity = discord.Game(name="Was Einstein's theory good? Relatively.", type=3)
    await client.change_presence(activity=activity)


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
    elif "/" not in pronouns:
      await ctx.send("Make sure the pronouns are formatted as \"a/b\"!")
    else:
        await ctx.guild.create_role(name=pronouns)
        await ctx.send(f"Pronouns \"{pronouns}\" have been added!")

@client.command()
async def pronounList(ctx):
  pronouns = "Pronouns available are:\n"
  for i in ctx.guild.roles:
    if "/" in i.name:
      pronouns= pronouns+(i.name)+"\n"
  await ctx.send(f"```{pronouns}```")

@client.command()
async def ping(ctx):
    await ctx.send("Pong!")
    print("pang")

my_secret = os.environ['TOKEN']
client.run(my_secret)

#load_dotenv(".env")
#client.run(os.getenv("TOKEN"))
