import discord
from discord.ext import commands
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Create a bot instance
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    logging.info(f'Logged in as {bot.user.name}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    logging.info(f'Message from {message.author}: {message.content}')
    await bot.process_commands(message)

@bot.command()
async def hello(ctx):
    await ctx.send('Hello! How can I assist you today?')

@bot.command()
async def upload(ctx):
    await ctx.send('Please upload a file to share.')

@bot.command()
async def echo(ctx, *, content: str):
    await ctx.send(content)

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

@bot.command()
async def log_file(ctx):
    file_path = 'path/to/your/file.txt'  # Change to the path of your file
    try:
        await ctx.send(file=discord.File(file_path))
        logging.info(f'Uploaded file: {file_path}')
    except Exception as e:
        logging.error(f'Failed to upload file: {e}')
        await ctx.send('Failed to upload file. Please check the logs.')

# Run the bot with your token
bot.run('YOUR_BOT_TOKEN')