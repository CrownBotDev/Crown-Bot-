# pet.py
import discord
from discord.ext import commands
import json
import os
import aiohttp
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.message_content = True  # Enable the message content intent

bot = commands.Bot(command_prefix='!', intents=intents)

class Pet:
    #pet data file
    PET_FILE = 'pets.json'
    pets = {}



    def __init__(self, name, hunger=50, happiness=50):
        self.name = name
        self.hunger = hunger
        self.happiness = happiness

    def feed(self):
        # Implement feed logic
        # For example, decrease hunger and increase happiness
        self.hunger -= 10
        self.happiness += 20

    def play(self):
        # Implement play logic
        # For example, decrease hunger and increase happiness
        self.hunger -= 5
        self.happiness += 30

        self.initialize()


    @staticmethod
    def load_pets():
        try:
            with open(Pet.PET_FILE, 'r') as file:
             data = json.load(file)
             print("Loaded pet data:", data)
             return data
        except (json.decoder.JSONDecodeError, FileNotFoundError):
            # Handle the case where the file is empty or malformed
            print("No pet data found or file is missing")
            return {}

    @staticmethod
    def save_pets():
        data = {user_id: pet.to_dict() for user_id, pet in Pet.pets.items()}
        with open(Pet.PET_FILE, 'w') as file:
            json.dump(data, file)

    @classmethod
    def initialize(cls):
        cls.pets = cls.load_pets()

    @classmethod
    def from_dict(cls, data):
        return cls(name=data["name"], hunger=data.get("hunger", 50), happiness=data.get("happiness", 50))

    def to_dict(self):
        return {
            "name": self.name,
            "hunger": self.hunger,
            "happiness": self.happiness
        }
    
    @classmethod
    def create_pet(cls, bot, user_id, name):
     if user_id not in cls.pets:
        new_pet = cls(name)
        cls.pets[user_id] = new_pet
        cls.save_pets()
        return new_pet
     else:
        return None
        
# Ensure that 'bot' is only imported when the file is run directly
if __name__ == "__main__":
    bot = commands.Bot(command_prefix='!', intents=intents)



