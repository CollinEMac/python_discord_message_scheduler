import os
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')

intents = discord.Intents.all()
# All command start with a "!"
client = commands.Bot(command_prefix="!", intents=intents)

message = ""
channel = None

def set_channel_and_message(ctx, msg_fragments):
    """
    Set the message and channels so the tasks have access to them.
    """
    global message
    for fragment in msg_fragments:
        message += fragment + " "
    global channel
    channel = ctx.channel

@client.event
async def on_ready():
    """
    Make sure the client is up and running before interacting with it
    """
    print('Bot Online.')

# @client.command(name="test_message")
# async def test_message(ctx, msg):
#     """
#     Test message command (for testing only unless you're really annoying)
#     """
#     set_channel_and_message(ctx, msg)
#     test_job.start()
#     await channel.send('Created a test message')

@client.command(name="daily_message")
async def daily_message(ctx, *args):
    """
    Command to set a daily message
    """
    set_channel_and_message(ctx, args)
    daily_job.start()
    await channel.send('Created a daily message')

@client.command(name="weekly_message")
async def weekly_message(ctx, *args):
    """
    Command to set a weekly message
    """
    set_channel_and_message(ctx, args)
    weekly_job.start()
    await channel.send('Created a weekly message')

# @tasks.loop(minutes=1)
# async def test_job():
#     await channel.send(message)

@tasks.loop(hours=24)
async def daily_job():
    await channel.send(message)

@tasks.loop(hours=168)
async def weekly_job():
    await channel.send(message)

client.run(TOKEN)
