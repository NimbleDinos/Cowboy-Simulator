# Discord Imports
import discord
import discord.ext
from discord.ext.commands import Bot
from discord.ext import commands 

# Other Files Imports
import player
import ability

bot_prefix = "!"
client = commands.Bot(command_prefix=bot_prefix)
client.remove_command("help")

@client.event
async def on_ready():
	print("Bot is online")
	print("Name: Cowboy Simulator")
	print("TD: {}".format(client.user.id))

@client.command()
async def test(ctx):
	await ctx.send("Hello, this is a test!")

@client.event
async def on_message(message):
	if message.author.bot:
	    return

	# THIS THING FUCKING DONT WORK
	if "a" in message.content.lower():
		thing = message.server.members
		for x in thing:
			print(x)
	
	await client.process_commands(message)

file = open("token.txt", "r")
token = str(file.read())
file.close()
client.run(token)