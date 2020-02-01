# Discord Imports
import discord
import discord.ext
from discord.ext.commands import Bot
from discord.ext import commands

# Other Files Imports
import player
import ability
import APIMethods

import db

bot_prefix = "!"
client = commands.Bot(command_prefix=bot_prefix)
client.remove_command("help")

# global variables
playerList = []

database_loc = r"./db/database.sql"
database = db.database.Database(database_loc)
database.create_player_table()

# bot startup messages
@client.event
async def on_ready():
	print("Bot is online")
	print("Name: Cowboy Simulator")
	print("TD: {}".format(client.user.id))


# test command
@client.command()
async def test(ctx):
	await ctx.send("Hello, this is a test!")


# join game command
@client.command()
async def join(ctx):
	userID = ctx.message.author.id
	userName = ctx.message.author.name

	result = database.select_player(userID)

	if len(result) == 1:
		# user is already in database
		await ctx.send("You are already in the game " + userName + "!")
	else:
		# add user to game database
		player_data = userID
		database.add_player(player_data)
		newPlayer = player.playerClass()
		newPlayer.id = userID
		playerList.append(newPlayer)
		await ctx.send("You have joined the game " + userName + "!")


# go to command
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
