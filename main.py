from discord import channel, client, guild
from dotenv import load_dotenv
import os
import json
import discord
import requests
import asyncio
from twitchAPI.twitch import Twitch
from discord.ext import commands, tasks
from discord.utils import get

intents = discord.Intents.all()
client = commands.Bot(command_prefix="$", intents=intents)

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


def isLive(username):
    URL = "https://id.twitch.tv/oauth2/token"
    CLIENT_ID = os.environ['CLIENT_ID']
    CLIENT_SECRET = os.environ['CLIENT_SECRET']
    GRANT_TYPE = "client_credentials"
    PARAMS = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": GRANT_TYPE
    }

    r1 = requests.post(url=URL, params=PARAMS)
    token = r1.json()["access_token"]

    URL2 = "https://api.twitch.tv/helix/search/channels?query=" + username
    HEADERS = {"client-id": CLIENT_ID, "Authorization": f"Bearer {token}"}

    r2 = requests.get(url=URL2, headers=HEADERS)

    data = r2.json()

    for i in range(len(data["data"])):
        if (data["data"][i]["broadcaster_login"]) == username or (
                data["data"][i]["display_name"]) == username:
            return [(data["data"][i]["is_live"]), (data["data"][i]["title"]),
                    (data["data"][i]["game_name"])]


@client.command()
@commands.has_role("Admin")
async def liveLoop(ctx, username):
    await ctx.send(f"LiveLoop tracking started on {username}")
    while True:
        check = isLive(username)
        guild = client.get_guild(802943410313887774)
        channel = guild.get_channel(802959911067320321)
        if check[0] == True:
            embed = discord.Embed(
                title=f"🔴 Reisu1337 is now Live - {check[1]}",
                url="https://twitch.tv/reisu1337",
                description=
                "Reisu1337 is now live! Click the link above to join and say hi!",
                color=0xcf332a)
            embed.set_thumbnail(
                url=
                "https://static-cdn.jtvnw.net/jtv_user_pictures/740ff158-a50d-4410-95d8-516b8d24b4f6-profile_image-300x300.png"
            )
            embed.set_image(
                url=
                "https://static-cdn.jtvnw.net/previews-ttv/live_user_reisu1337-1280x720.jpg"
            )
            embed.set_footer(text="ReisuBot#2243")
            await channel.send("@everyone", embed=embed)
            break
        else:
            pass
        await asyncio.sleep(10)


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
            await ctx.send(
                "These pronouns haven't been added yet, ask a mod to add them for you!"
            )
    else:
        await ctx.send("Make sure your pronouns are formatted as \"a/b\"!")

@client.command()
async def hi(ctx):
	user = ctx.message.author
	await ctx.send(f"Hello, {user.mention}")



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
            pronouns = pronouns + (i.name) + "\n"
    await ctx.send(f"```{pronouns}```")


@client.command()
async def ping(ctx):
    await ctx.send("Pong!")
    print("Pang!")


my_secret = os.environ['TOKEN']
client.run(my_secret)

#load_dotenv(".env")
#client.run(os.getenv("TOKEN"))
