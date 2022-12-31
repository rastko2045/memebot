import discord
import os
from dotenv import load_dotenv
from discord.ext import commands

from meme import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
memes_dir = os.getenv('MEME_DIR')


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents, description= "This is a test bot")

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if "medhi" in message.content.lower():
        print("Medhi detected: (╯°□°）╯︵ ┻━┻!")
        await message.channel.send('(╯°□°）╯︵ ┻━┻')
    await bot.process_commands(message)

@bot.command()
async def meme(ctx, memeName : str, text : str):
    print("Image request received for " + memeName + " with text " + text)
    """Creates Image"""
    create_meme(memeName, text)
    await ctx.send(file=discord.File(get_meme_path("temp")))
    delete_meme()

@bot.command()
async def mehdi(ctx):
    print("Image request received for mehdi")
    """Creates Image"""
    await ctx.send(file=discord.File(get_meme_path("angry_mehdi")))


bot.run(TOKEN)