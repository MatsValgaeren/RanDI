import discord
from discord.ext import commands
import logging
import os
import random
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('DISCORD_TOKEN')
img_path = os.getenv('IMAGE_PATH')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user.name} is ready!")

@bot.command()
async def img(ctx):
    rand_img = get_rand_img()
    if not os.path.exists(rand_img):
        await ctx.send("Image not found.")
        return

    with open(rand_img, 'rb') as f:
        picture = discord.File(f)
        await ctx.send(file=picture)

def get_rand_img():
    files = os.listdir(img_path)
    n = len(files)
    rand_image = files[random.randint(0, n - 1)]
    print(rand_image)
    return os.path.join(img_path, rand_image)

bot.run(token, log_handler=handler, log_level=logging.DEBUG)