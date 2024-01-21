# tester.py
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from pet_class import Pet
from Commands import MyCog  # Import the bot instance from commands.py
import atexit
import aiohttp
import asyncio
from pet_cog import PetCog

# Declare session as a global variable
session = None

# Load environmet variables from .env
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
YOUR_BOT_OWNER_ID = os.getenv("OWNER_ID")  # Bot owner User-ID

# Ensure the bot token is set and run the bot
intents = discord.Intents.default()
intents.message_content = True  # Enable message-related events
intents.members = True  # Enable member-related events

# Create an instance of commands.Bot
bot = commands.Bot(command_prefix="!", intents=intents)  # Set your desired command prefix and include intents

bot.load_extension('pet_cog')
print("Loaded commands:", [command.name for command in bot.commands])

# Print a message to indicate that the cog is loaded
print("Cog (commands) loaded successfully")

# Set the cooldown duration in seconds (e.g., 8 hours)
COOLDOWN_DURATION = 8 * 60 * 60

# Dictionary to store users' credits
user_credits = {}

# Standard amount of credits to give
standard_credits = 1000

# Last usage of !daily
last_daily_usage = {}

# Dictionary to store users' leaderboard positions
leaderboard = {}

# Define a dictionary to keep track of milestones for each user
user_milestones = {}

# Now, include the imported class from pet.py
pet_instance = None


# Access the feed_pet and play_with_pet methods
if pet_instance:
    pet_instance.feed()  # Example of using feed_pet
    pet_instance.play()  # Example of using play_with_pet
else:
    print("Pet instance is none. Make sure to create a pet first.")

# Event: Trigger on bot ready
@bot.event
async def on_ready():
    print("on_ready event called!")
    print(f"Logged in as {bot.user.name} ({bot.user.id})")

    Pet.initialize()

    # Access the pet instance from the dictionary
    global pet_instance
    pet_instance = Pet.pets.get(bot.user.id)

    if pet_instance:
        print("Pet instance found")
        print(f"Pet details: Name - {pet_instance.name}, Hunger - {pet_instance.hunger}, Happiness - {pet_instance.happiness}")
        # Example of using feed_pet and play_with_pet methods
        pet_instance.feed()  # Example of using feed_pet
        pet_instance.play()  # Example of using play_with_pet
    else:
        print("Pet instance not found.")
        print("Pet.pets dictionary contents:", Pet.pets)


@bot.event
async def on_connect():
    print("Bot connected to Discord.")
    Pet.pets.update(Pet.load_pets())
    bot.session = aiohttp.ClientSession()

@bot.event
async def on_disconnect():
    print("Bot disconnected from Discord.")
    Pet.save_pets()

@bot.event
async def on_exit():
    print("Bot exiting. Performing cleanup tasks...")
    Pet.save_pets()
    if bot.session and not bot.session.closed:
        await bot.session.close()



# Command : Disconnect bot, only owner permitted
@bot.command(name='disconnect', hidden=True)
async def disconnect_bot(ctx):
    try:
        # Check if the command invoker has the necessary permissions (optional)
        if ctx.author.id == int(YOUR_BOT_OWNER_ID):
            await ctx.send("Disconnecting... :wave:")
            Pet.save_pets()  # Save pets before disconnecting
            await bot.close()  # Close the bot connection
        else:
            await ctx.send("You don't have permission to use this command.")
    except Exception as e:
        print(f"An error occurred during bot disconnection: {e}")

async def on_exit():
    print("Bot exiting. Performing cleanup tasks...")
    # Add your cleanup tasks here, such as saving data or closing connections
    if bot.session and not bot.session.closed:
        await bot.session.close()

# Register the cleanup function to be called on script exit
atexit.register(lambda: asyncio.run(on_exit()))

# Run the bot with your token
bot.run(BOT_TOKEN)









