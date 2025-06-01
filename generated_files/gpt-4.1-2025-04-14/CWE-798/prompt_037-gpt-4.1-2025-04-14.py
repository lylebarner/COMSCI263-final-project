import discord
from discord.ext import commands
import logging

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    filename='bot_logs.log',
    filemode='a',
    format='%(asctime)s:%(levelname)s:%(name)s: %(message)s'
)

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Event: Log all messages
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    log_msg = f"{message.author} in {message.channel}: {message.content}"
    logging.info(log_msg)
    await bot.process_commands(message)

# Command: Respond to ping
@bot.command(name='ping')
async def ping_cmd(ctx):
    await ctx.send('Pong!')

# Command: Echo
@bot.command(name='echo')
async def echo_cmd(ctx, *, text: str):
    await ctx.send(f'You said: {text}')

# Command: Upload a file
@bot.command(name='upload')
async def upload_cmd(ctx):
    file_path = 'example.txt'
    try:
        with open(file_path, 'w') as f:
            f.write('Hello from the Discord bot!')
        await ctx.send('Here is your file:', file=discord.File(file_path))
    except Exception as e:
        await ctx.send(f'Failed to upload file: {e}')

# Run the bot
bot.run('YOUR_BOT_TOKEN_HERE')
