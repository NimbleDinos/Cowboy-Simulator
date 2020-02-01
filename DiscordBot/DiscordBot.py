# Discord Imports
import discord
import discord.ext
from discord.ext.commands import Bot
from discord.ext import commands 

# Other Files Imports
import player
import ability
import APIMethods

bot_prefix = "!"
client = commands.Bot(command_prefix=bot_prefix)
client.remove_command("help")

# global variables
playerList = []

@client.event
async def on_ready():
	print("Bot is online")
	print("Name: Cowboy Simulator")
	print("TD: {}".format(client.user.id))

@client.command()
async def test(ctx):
	await ctx.send("Hello, this is a test!")


@client.command()
async def join(ctx):
	userID = ctx.message.author.id
	userName = ctx.message.author.name

	if userID == 69420:
		# user is already in database
	    
		await ctx.send("You are already in the game " + userName + "!")
	else:
		# add user to game database
		newPlayer = player.playerClass()
		newPlayer.id = userID
		playerList.append(newPlayer)
		await ctx.send("You have joined the game " + userName + "!")

@client.command()
async def goto(ctx, location):
	userID = ctx.message.author.id
	userName = ctx.message.author.name

	for player in playerList:
		if player.id == userID:
			returnCheck = player.goToLocation(location)
			if returnCheck == 0:
			    await ctx.send("You are moving to: " + location + ", " + userName)
			if returnCheck == 1:
				await ctx.send("That's an invalid input partner " + userName)

@client.event
async def on_message(message):
	if message.author.bot:
	    return
	
	await client.process_commands(message)

file = open("token.txt", "r")
token = str(file.read())
file.close()
client.run(token)