import json
import logging
import os
import random

from dotenv import load_dotenv
import discord
from discord.ext import commands

import asyncio

import personal_commands

load_dotenv()

token = os.getenv('DISCORD_TOKEN')

img_path = os.getenv('IMAGE_PATH')
vid_path = os.getenv('VIDEO_PATH')
combo_names = os.getenv('FILE_NAME_COMBO')
accepted_names = os.getenv('ACCEPTED_NAMES').split(',')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

personal_commands.setup(bot)

def letter_to_emoji(letter):
    letter = letter.upper()
    if 'A' <= letter <= 'Z':
        base = 0x1F1E6  # Unicode for 🇦
        return chr(base + ord(letter) - ord('A'))
    return letter  # fallback if it's not A–Z

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
    rand_vid = get_rand_video()
    if not os.path.exists(rand_vid):
        await ctx.send("Image not found.")
        return

    with open(rand_vid, 'rb') as f:
        picture = discord.File(f)
        await ctx.send(file=picture)

@bot.command()
async def quiz(ctx):
    rand_img = get_rand_img()
    while not get_author_combo(rand_img):
        rand_img = get_rand_img()
    author_vid = get_author_combo(rand_img)

    if not os.path.exists(rand_img):
        await ctx.send("Image not found.")
        return

    with open(rand_img, 'rb') as f:
        picture = discord.File(f)

    question = "🧠 **Quiz Time!**\nWho posted this image?"

    options = []
    emojis = []
    correct_emoji = None
    print(accepted_names)
    for name in accepted_names:
        emoji = letter_to_emoji(name[0:1])
        option = emoji + ' ' + name
        emojis.append(emoji)
        options.append(option)
        if name == author_vid:
            correct_emoji = emoji

    quiz_msg = await ctx.send(
        content=f"{question}\n\n" + "\n".join(options),
        file=picture
    )

    for emoji in emojis:
        await quiz_msg.add_reaction(emoji)

    await asyncio.sleep(10)

    quiz_msg = await ctx.channel.fetch_message(quiz_msg.id)

    results = {}
    for reaction in quiz_msg.reactions:
        if reaction.emoji in emojis:
            voters = []
            async for user in reaction.users():
                if not user.bot:
                    voters.append(user)
            results[reaction.emoji] = len(voters)

    res = correct_emoji + ' ' + author_vid

    result_lines = []
    for emoji in emojis:
        count = results.get(emoji, 0)
        correct = "✅" if emoji == correct_emoji else ""
        result_lines.append(f"{emoji} - {count} votes {correct}")

    await ctx.send("The correct answer was: " + f"**{res}**")

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

def get_author_combo(file_path):
    with open(combo_names, 'r') as f:
        combos = json.load(f)

    base_name = os.path.basename(file_path)
    name, ext = os.path.splitext(base_name)
    file_name = name[:-6] + ext
    if combos[file_name]:
        return combos[file_name]
    else:
        return None

bot.run(token, log_handler=handler, log_level=logging.DEBUG)