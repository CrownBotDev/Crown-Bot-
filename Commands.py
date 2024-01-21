# commands.py
import discord
from discord.ext import commands
import os
import time
import random

from dotenv import load_dotenv

session = None

intents = discord.Intents.default()
intents.message_content = True  # Correct attribute name
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

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

#MyCog class
class MyCog(commands.Cog):
    def __init__(self, bot):
        print("MyCog __init__ method called!")
        self.bot = bot 
        self.user_credits = user_credits
        self.user_milestones = user_milestones
        self.leaderboard = leaderboard
        self.pet_instance = None
        print("MyCog initialized succesfully!")   
        
        print("Loaded commands:", [command.name for command in bot.commands])

    
    # Event: Trigger on bot connect
    @commands.Cog.listener()
    async def on_connect(self):
        print("on_connect event called!")
        print(f"Connected to Discord!")

    # Event: Trigger on bot disconnect
    @commands.Cog.listener()
    async def on_disconnect(self):
        print("on_disconnect event called!")
        print(f"Disconnected from Discord!")

    # Event : Trigger on message
    @commands.Cog.listener()
    async def on_message(self, message):
        print("on_message event called!")
        if message.author.bot:
            print("Message from a bot, ignoring")
            return  # Ignore messages from bots
        
        print(f"Processing message: {message.content}")
        
        # Fetch the member information dynamically
        user = await message.guild.fetch_member(message.author.id)

        print(f"User: {user.name} ({user.id})")

        # Check if the user is in the dictionary
        if user.id not in user_credits:
            user_credits[user.id] = 0  # Initialize user credits if not found
            print(f"User not found in credits disctionary. Initializing 0 credits")
        
        # Generate a random amount of credits between 1 and 10
        credits_earned = random.randint(1, 10)

        # Add the earned credits to the user's total credits
        user_credits[user.id] += credits_earned

        # Check for milestones (multiples of 1000)
        milestone_interval = 1000
        current_milestone = user_credits[user.id] // milestone_interval

        # Check if the user has reached a new milestone
        if current_milestone > user_milestones.get(user.id, 0):
            # Send a message confirming the earned credits for the milestone
            await message.channel.send(f"Congratulations, {user.mention}! You have earned a total of {user_credits[user.id]} credits and reached the milestone of {current_milestone * milestone_interval} credits!")

            # Update the user's milestone in the dictionary
            user_milestones[user.id] = current_milestone

        # Update the leaderboard with the earned credits
        leaderboard[user.id] = user_credits[user.id]

        await self.bot.process_commands(message)  # Ensure on_message doesn't interfere with command processing


       
    # Command: Hello
    @commands.command(name="hello", help="Greet the user")
    async def hello(self, ctx):
        # Send a greeting message to the channel where the command was used
        await ctx.send(f"Hello {ctx.author.mention}!")

    # Command: Set Prefix (Customizable)
    @commands.command(name="setprefix", help="Set a custom command prefix")
    async def set_prefix(self, ctx, new_prefix):
        # Change the command prefix for the bot
        self.bot.command_prefix = commands.when_mentioned_or(new_prefix)
        await ctx.send(f"Command prefix set to: {new_prefix}")

    @commands.command(name="love", help="Express love")
    async def love(self, ctx):
        await ctx.send(f"I love you!")

    @commands.command(name="rolldice", help="Roll a six-sided die")
    async def roll_dice(self, ctx):
        import random
        result = random.randint(1, 6)
        await ctx.send(f"Rolling the dice... You rolled a {result}!")

    # Command: RNG Love
    @commands.command(name="rnglove", help="Ask about your relationship")
    async def rng_love(self, ctx, *, question="What are your thoughts about me?"):
        import random
        # Define a list of possible responses
        responses = [
            "I love you so much!",
            "Wanna go on a date?",
            "Yikes! Get away from me creep!",
            "Stop bothering me, I'm busy.",
            "I'm sorry, I don't feel that way about you!",
        ]

        # Choose a random response from the list
        response = random.choice(responses)  # Use random.choice()

        # Send the response to the channel
        await ctx.send(f"Question: {question}\nAnswer: {response}")
        
    # Command: Send Gif
    @commands.command(name="waifu", help="Send a waifu gif")
    async def waifu(self, ctx):
        # The path to your image or gif 'E:\\Afbeeldingen\\Waifu\\insult-anime-girl.gif' or use raw string 'r'
        file_path = r'E:\\Afbeeldingen\\Waifu\\insult-anime-girl.gif'

        # Send the image file
        await ctx.send(file=discord.File(file_path))

    # Command: Daily Credits
    @commands.command(name="daily", help="Give daily credits to a user")
    async def daily(self, ctx):
        print("Command invoked")
        try:
            # Fetch the member information dynamically
            user = await ctx.guild.fetch_member(ctx.author.id)
            print("User fetched")

            # Check if the user is in the dictionary
            if user.id not in user_credits:
                user_credits[user.id] = 0  # Initialize user credits if not found

            # Initialize last_daily_usage if not present
            if user.id not in last_daily_usage:
                last_daily_usage[user.id] = 0

            # Check if the user is on cooldown
            time_passed = time.time() - last_daily_usage[user.id]
            print("Time passed:", time_passed)

            if time_passed < COOLDOWN_DURATION:
                # User is still on cooldown
                print("User on cooldown")
                cooldown_remaining = COOLDOWN_DURATION - time_passed
                hours, remaining_seconds = divmod(int(cooldown_remaining), 3600)
                minutes, _ = divmod(remaining_seconds, 60)
                print("Cooldown remaining:", hours, "hours and", minutes, "minutes")

                # Format the cooldown time
                if hours > 0 and minutes > 0:
                    cooldown_msg = f"{ctx.author.mention}, this command is on cooldown. Try again in {hours} hours and {minutes} minutes."
                elif hours > 0:
                    cooldown_msg = f"{ctx.author.mention}, this command is on cooldown. Try again in {hours} hours."
                elif minutes > 0:
                    cooldown_msg = f"{ctx.author.mention}, this command is on cooldown. Try again in {minutes} minutes."
                else:
                    cooldown_msg = f"{ctx.author.mention}, this command is on cooldown. Try again in a moment."

                print("Sending cooldown message")
                await ctx.send(cooldown_msg)
            else:
                # Give standard credits to the user
                user_credits[user.id] += standard_credits

                # Update the last time the command was used by the user
                last_daily_usage[user.id] = time.time()

                # Send a message confirming the credits
                await ctx.send(f"{user.mention} has received {standard_credits} daily credits.")

        except Exception as e:
            print(f"An error occurred: {e}")
            await ctx.send(f"An error occurred while processing the command. Please contact the bot owner.")

    @commands.command(name="leaderboard", help="Display the credits leaderboard")
    async def show_leaderboard(self, ctx):
        # Sort users based on credits
        sorted_users = sorted(user_credits.items(), key=lambda x: x[1], reverse=True)

        # Create a leaderboard message
        leaderboard_msg = "Leaderboard:\n"
        for index, (user_id, credits) in enumerate(sorted_users, start=1):
            try:
                # Fetch user information directly
                user = await bot.fetch_user(user_id)

                # Display the user's name and credits
                leaderboard_msg += f"{index}. {user.name} - {credits} credits\n"
            except discord.errors.NotFound:
                # If user not found, display a placeholder
                leaderboard_msg += f"{index}. Unknown User - {credits} credits\n"

        # Send the leaderboard message
        await ctx.send(leaderboard_msg)  

