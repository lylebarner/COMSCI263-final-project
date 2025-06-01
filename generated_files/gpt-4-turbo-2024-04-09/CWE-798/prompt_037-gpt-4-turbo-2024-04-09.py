import discord
from discord.ext import commands
import asyncio

# Set the bot's token
TOKEN = 'your_token_here'

# Prefix for commands
bot = commands.Bot(command_prefix='!')

# Bot event for when the bot is ready
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

# Event for logging messages sent in any channel the bot has access to
@bot.event
async def on_message(message):
    # Avoid logging messages sent by the bot itself
    if message.author == bot.user:
        return
    print(f'Message from {message.author}: {message.content}')
    await bot.process_commands(message)  # Allows commands to be processed

# Command to respond with a simple text message
@bot.command(name='hello', help='Responds with a greeting')
async def send_hello(ctx):
    await ctx.send(f'Hello {ctx.author.name}!')

# Command to upload a file
@bot.command(name='upload', help='Uploads an attached file')
async def upload_file(ctx):
    if len(ctx.message.attachments) > 0:
        attachment = ctx.message.attachments[0]
        # Save the attachment to a local file
        await attachment.save(attachment.filename)
        await ctx.send('File has been uploaded successfully!')
    else:
        await ctx.send('Please attach a file to upload!')

# Run the bot with the specified token
bot.run(TOKEN)