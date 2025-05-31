import discord

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('Bot is ready')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        await message.channel.send('Hello!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!upload'):
        await message.channel.send('Please upload a file.')

client.run('YOUR_DISCORD_BOT_TOKEN')