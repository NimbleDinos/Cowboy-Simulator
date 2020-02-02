import datetime
import asyncio

# Discord Imports
import discord
import discord.ext
from discord.ext.commands import Bot
from discord.ext import commands

# Other Files Imports
import player
import ability
import APIMethods
import logisticFunc

import db

locationList = ["hull", "lincoln", "sheffield", "corral", "gold-mine", "plains", "river", "shooting-range", "travelling"]

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

	client.loop.create_task(update())

# Update loop
async def update():
	while True:
		print("Test")
		await asyncio.sleep(1)

# test command
@client.command()
async def test(ctx):
	await ctx.send("Hello, this is a test!")
	userID = ctx.message.author.id
	userName = ctx.message.author.name
	
	me = player.playerClass()
	

# join game command
@client.command()
async def join(ctx):
	userID = ctx.message.author.id
	userName = ctx.message.author.name

	player_exist = database.select_player_exists(userID)
	# print(player_exist)
	print("in command")

	if (len(player_exist)) == 0:
		player_data = (userID, 1)
		database.add_player(player_data)
		newPlayer = player.playerClass()
		newPlayer.id = userID
		playerList.append(newPlayer)
		api_message = APIMethods.join_game_request(userID, userName)
		await ctx.send(api_message)
	else:
		player_status = database.select_player_status(userID)
		print(player_status[0])
		if player_status[0] == (0,):
			database.update_player_status(userID, 1)
			api_message = APIMethods.join_game_request(userID, userName)
			await ctx.send(api_message)
		else:
			await ctx.send("You are already in the game " + userName + "!")

@client.command()
async def leave(ctx):
	user_id = ctx.message.author.id
	user_name = ctx.message.author.name

	player_exist = database.select_player_exists(user_id)
	if (len(player_exist)) == 0:
		await ctx.send("You are not currently in the game " + user_name +"!")
	else:
		player_status = database.select_player_status(user_id)
		if player_status[0] == (0,):
			await ctx.send("You are not currently in the game " + user_name + "!")
		else:
			database.update_player_status(user_id, 0)
			APIMethods.join_game_request(user_id, user_name)
			await ctx.send("See you soon " + user_name +"!")

# go to command
@client.command()
async def goto(ctx, location):
	userID = ctx.message.author.id
	userName = ctx.message.author.name

	player_status = database.select_active_players(userID)
	print(player_status)
	if player_status[0] == (1,):
		if location.lower() in locationList:
			# TODO: update db with new loc
			#TODO: do thing to get time here
			time = 30
			api_message = APIMethods.move_to_request(userID, location.lower(), time)
			await ctx.send(api_message)
		else:
			await ctx.send("Sorry but {0} isn't a valid place".format(location.lower()))
	else:
		await ctx.send("You aren't in the game yet, {0}".format(userName))

@client.event
async def on_message(message):
	if message.author.bot:
		return

	await client.process_commands(message)

file = open("token.txt", "r")
token = str(file.read())
file.close()
client.run(token)