import discord
import discord.ext
from discord.ext.commands import Bot
from discord.ext import commands 

bot_prefix = "!"
client = commands.Bot(command_prefix=bot_prefix)
client.remove_command("help")

@client.event
async def on_ready():
	print("Bot is online")
	print("Name: Cowboy Simulator")
	print("TD: {}".format(client.user.id))

file = open("token.txt", "r")
token = str(file.read())
file.close()
client.run(token)