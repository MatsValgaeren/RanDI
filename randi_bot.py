import discord
from discord.ext import commands
import logging
import os
import random
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('DISCORD_TOKEN')
img_path = os.getenv('IMAGE_PATH')
elli_path = os.getenv('ELLI_PATH')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_command_error(ctx, error):
    await ctx.send(f"Error: {str(error)}")
    print(f"Error in command {ctx.command}: {error}")

@bot.event
async def on_ready():
    print(f"{bot.user.name} is ready!")
    print(f"Image path: {img_path}")

@bot.command()
async def img(ctx):
    rand_img = get_rand_img(img_path)
    if not os.path.exists(rand_img):
        await ctx.send("Image not found.")
        return

    with open(rand_img, 'rb') as f:
        picture = discord.File(f)
        await ctx.send(file=picture)

@bot.command()
async def spam(ctx):
    for i in range(10):
        rand_img = get_rand_img(img_path)
        if not os.path.exists(rand_img):
            await ctx.send("Image not found.")
            return

        with open(rand_img, 'rb') as f:
            picture = discord.File(f)
            await ctx.send(file=picture)

@bot.command()
async def elli(ctx):
    rand_img = get_rand_img(elli_path)
    if not os.path.exists(rand_img):
        await ctx.send("Image not found.")
        return

    with open(rand_img, 'rb') as f:
        picture = discord.File(f)
        await ctx.send(file=picture)

def get_rand_img(file_path):
    files = os.listdir(file_path)
    n = len(files)
    rand_image = files[random.randint(0, n - 1)]
    print(rand_image)
    return os.path.join(file_path, rand_image)

bot.run(token, log_handler=handler, log_level=logging.DEBUG)