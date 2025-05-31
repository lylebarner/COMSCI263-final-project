import discord
from discord.ext import commands
import logging
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(name)s: %(message)s',
    handlers=[
        logging.FileHandler(filename='bot.log', encoding='utf-8', mode='a'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('discord')

# Define intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True

# Initialize bot
bot = commands.Bot(command_prefix='!', intents=intents)

# Event: on_ready
@bot.event
async def on_ready():
    logger.info(f'Logged in as {bot.user} (ID: {bot.user.id})')
    logger.info('------')

# Event: on_message
@bot.event
async def on_message(message):
    if message.author.bot:
        return
    logger.info(f'Message from {message.author} in {message.guild}/{message.channel}: {message.content}')
    if message.attachments:
        for attachment in message.attachments:
            logger.info(f'Attachment: {attachment.url}')
    await bot.process_commands(message)

# Command: ping
@bot.command(name='ping')
async def ping(ctx):
    await ctx.send('Pong!')
    logger.info(f'Ping command invoked by {ctx.author}')

# Command: upload
@bot.command(name='upload')
async def upload(ctx):
    file_path = 'sample.txt'  # Replace with your file path
    if os.path.isfile(file_path):
        with open(file_path, 'rb') as f:
            discord_file = discord.File(f)
            await ctx.send('Here is your file:', file=discord_file)
            logger.info(f'File {file_path} uploaded by {ctx.author}')
    else:
        await ctx.send('File not found.')
        logger.warning(f'File {file_path} not found for upload by {ctx.author}')

# Run the bot
TOKEN = 'YOUR_BOT_TOKEN_HERE'  # Replace with your Discord bot token
bot.run(TOKEN)