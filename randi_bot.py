import json
import logging
import os
import random

from dotenv import load_dotenv
import discord
from discord.ext import commands

import personal_commands

load_dotenv()

token = os.getenv('DISCORD_TOKEN')

img_path = os.getenv('IMAGE_PATH')
vid_path = os.getenv('VIDEO_PATH')


handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

personal_commands.setup(bot)

@bot.event
async def on_command_error(ctx, error):
    await ctx.send(f"Error: {str(error)}")
    print(f"Error in command {ctx.command}: {error}")

@bot.event
async def on_ready():
    print(f"{bot.user.name} is ready!")
    print(f"Image path: {img_path}")
    print(f"Video path: {vid_path}")

@bot.command()
async def img(ctx):
    rand_img = get_rand_img()
    if not os.path.exists(rand_img):
        await ctx.send("Image not found.")
        return

    with open(rand_img, 'rb') as f:
        picture = discord.File(f)
        await ctx.send(file=picture)

@bot.command()
async def spam(ctx):
    for i in range(10):
        rand_img = get_rand_img()
        if not os.path.exists(rand_img):
            await ctx.send("Image not found.")
            return

        with open(rand_img, 'rb') as f:
            picture = discord.File(f)
            await ctx.send(file=picture)

@bot.command()
async def vid(ctx):
    print('start')
    rand_vid = get_rand_video()
    if not os.path.exists(rand_vid):
        await ctx.send("Image not found.")
        return

    with open(rand_vid, 'rb') as f:
        picture = discord.File(f)
        await ctx.send(file=picture)

def get_rand_img():
    print('opening')
    with open('image_names.json', 'r') as f:
        files = json.load(f)

    n = len(files)
    print('get rand')
    rand_image = files[random.randint(0, n - 1)]
    print(rand_image, 'send')
    return os.path.join(img_path, rand_image)

def get_rand_video():
    with open('video_names.json', 'r') as f:
        files = json.load(f)

    n = len(files)
    rand_video = files[random.randint(0, n - 1)]
    return os.path.join(vid_path, rand_video)

bot.run(token, log_handler=handler, log_level=logging.DEBUG)