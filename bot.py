import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from io import BytesIO

from meme import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents, description= "Allows users to save and caption memes.")

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
async def caption(ctx, memeName : str = None, *, text : str = None):
    """Captions a meme: !caption <memeName> <text>"""
    if memeName is None or text is None:
        await ctx.send("Correct usage: !caption <memeName> <text>. For a list of available memes use !list.")
        return
    print("Image request received for " + memeName + " with text " + text + ". From server " + ctx.guild.name + " by " + ctx.author.name + " in channel " + ctx.channel.name)
    try:
        img = create_meme(memeName, text)
    except FileNotFoundError:
        await ctx.send("Meme " + memeName + " does not exist. For a list of available memes use !list.")
    except ValueError:
        await ctx.send("There are no path traversal attacks here. Please stop trying to break me.")
    except:
        await ctx.send("Something went wrong. Please report this.")
        print(getMemes())
    else:
        with BytesIO() as image_binary:
            img.save(image_binary, 'JPEG')
            image_binary.seek(0)
            await ctx.send(file=discord.File(fp=image_binary, filename=memeName+".jpeg"))

@bot.command()
async def meme(ctx, memeName : str = None):
    """Shows a meme format: !meme <memeName>"""
    if memeName is None:
        await ctx.send("Correct usage: !meme <memeName>. For a list of available memes use !list.")
        return
    print("Image request received for " + memeName + ". From server " + ctx.guild.name + " by " + ctx.author.name + " in channel " + ctx.channel.name)
    try:
        img = open_meme(memeName)
    except FileNotFoundError:
        await ctx.send("Meme " + memeName + " does not exist. For a list of available memes use !list.")
    except ValueError:
        await ctx.send("There are no path traversal attacks here. Please stop trying to break me.")
    except:
        await ctx.send("Something went wrong. Please report this.")
        print(getMemes())
    else:
        with BytesIO() as image_binary:
            img.save(image_binary, 'JPEG')
            image_binary.seek(0)
            await ctx.send(file=discord.File(fp=image_binary, filename=memeName+".jpeg"))

@bot.command()
async def save(ctx, memeName : str = None):
    """Saves a new meme: !save <memeName>. Message must contain an image attachment"""
    if memeName is None:
        await ctx.send("Correct usage: !save <memeName>.")
        return
    print("New meme request: " + memeName + ". From server " + ctx.guild.name + " by " + ctx.author.name + " in channel " + ctx.channel.name)
    if(len(ctx.message.attachments) == 0):
        await ctx.send("No image attached. Use !help to see how to use this command.")
    elif(len(ctx.message.attachments) > 1):
        await ctx.send("Too many images attached. Use !help to see how to use this command.")
    elif(not ctx.message.attachments[0].content_type.startswith("image")):
        await ctx.send("Invalid attachment. Use !help to see how to use this command.")
    elif(ctx.message.attachments[0].size > 8388608):
        await ctx.send("Image size too big. Maximum size is 8MB.")
    else:
        try: 
            print("Saving meme " + memeName)
            await ctx.message.attachments[0].save(get_meme_path(memeName))
            await ctx.send("Meme " + memeName + " saved successfully.")
        except ValueError:
            await ctx.send("There are no path traversal attacks here. Please stop trying to break me.")
        except:
            await ctx.send("Something went wrong. Please report this.")
        

@bot.command()
async def delete(ctx, memeName : str = None):
    """Deletes a saved meme: !delete <memeName>"""
    if memeName is None:
        await ctx.send("Correct usage: !delete <memeName>. For a list of available memes use !list.")
        return
    print("Delete meme request: " + memeName)
    try:
        delete_meme(memeName)
    except ValueError:
        await ctx.send("There are no path traversal attacks here. Please stop trying to break me.")
    except:
        await ctx.send("Meme " + memeName + " does not exist. For a list of available memes use !list.")
    else:
        await ctx.send("Meme " + memeName + " deleted successfully.")

@bot.command()
async def list(ctx):
    """Lists all available memes"""
    print("List memes request")
    memes = getMemes()
    if(memes == ""):
        await ctx.send("No memes available. To add a new meme use !save <memeName>.")
    else:
        await ctx.send("Available memes:\n" + memes)

@bot.command()
async def mehdi(ctx):
    """:clueless:"""
    print("Image request received for mehdi")
    """Creates Image"""
    await ctx.send(file=discord.File(get_meme_path("angry_mehdi")))


bot.run(TOKEN)