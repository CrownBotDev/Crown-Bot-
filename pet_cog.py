import discord
from discord.ext import commands
from pet_class import Pet  # Assuming your Pet class is defined in pet.py

intents = discord.Intents.default()
intents.message_content = True  # Correct attribute name
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

class PetCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
     
    @classmethod 
    def setup(cls, bot):
        bot.add_cog(cls(bot))

    # Command: Create Pet
    @commands.command(name='createpet')
    async def create_pet_command(self, ctx, name=None):
        if name is None:
            # If name is not provided, send a message to the user
            await ctx.send("Please provide a name for your pet. Example: `!createpet MyPetName`")
            return
        
        if ctx.author.id in Pet.pets:
            # If the user already has a pet, send a message and return
            await ctx.send("You already have a pet.")
            return
        

        pet_instance = Pet.create_pet(self.bot, ctx.author.id, name)
        print(f"pet_instance: {pet_instance}")
        
        if pet_instance:
            # Store the pet instance in the Pet.pets dictionary
            Pet.pets[ctx.author.id] = pet_instance

       
            await ctx.send(f"You've adopted a pet named {name}! Take good care of it.")
            pet_instance.feed()
            pet_instance.play()
            Pet.save_pets()
            print("Saving pet data successful")
        else:
            await ctx.send("Failed to create a pet,")
    
    @commands.command(name='feed')
    async def feed_pet_command(self, ctx):
        pet = Pet.pets.get(ctx.author.id)
        if pet:
            pet.feed()
            Pet.save_pets()
            await ctx.send(f"You fed {pet.name}. Hunger: {pet.hunger}, Happiness: {pet.happiness}")
        else:
            await ctx.send("You don't have a pet. Adopt one using !createpet")

    @commands.command(name='play')
    async def play_with_pet_command(self, ctx):
        pet = Pet.pets.get(ctx.author.id)
        if pet:
            pet.play()
            Pet.save_pets()
            await ctx.send(f"You played with {pet.name}. Hunger: {pet.hunger}, Happiness: {pet.happiness}")
        else:
            await ctx.send("You don't have a pet. Adopt one using !createpet")

PetCog.setup(bot)