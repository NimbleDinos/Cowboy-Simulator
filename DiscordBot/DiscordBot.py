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
import random

locationList = ["hull", "lincoln", "sheffield", "corral", "gold-mine", "plains", "river", "shooting-range", "travelling"]

bot_prefix = "!"
client = commands.Bot(command_prefix=bot_prefix)
client.remove_command("help")

# global variables
active_player_list = []

database_loc = r"./db/database.sql"
database = db.database.Database(database_loc)
database.create_player_table()
database.create_inventory_table()
database.update_all_player_status()

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
		print(active_player_list)
		for person in active_player_list:
			location_obj = database.select_player_place(person.player_id)
			test = database.select_user_gold(person.player_id)
			print("GOLD {0}".format(test))
			(loc,) = location_obj[0]
			# do thing based on location
			if loc == "travelling":
				database.update_player_intown(person.player_id, True)
			if loc == "hull":
				database.update_player_intown(person.player_id, True)
				person.hatAction()
			if loc == "lincoln":
				database.update_player_intown(person.player_id, True)
				person.hatAction()
			if loc == "sheffield":
				database.update_player_intown(person.player_id, True)
				person.hatAction()
			if loc == "corral":
				database.update_player_intown(person.player_id, False)
				person.ridingAction()
			if loc == "gold-mine":
				print("IN IF")
				database.update_player_intown(person.player_id, False)
				person.mineAction()
			if loc == "plains":
				database.update_player_intown(person.player_id, False)
				person.catchAction()
			if loc == "river":
				database.update_player_intown(person.player_id, False)
				person.panAction()
			if loc == "shooting-range":
				database.update_player_intown(person.player_id, False)
				person.shootingAction()
			
			# update health
			person.healAction()

		print("Jobs Done")
		await asyncio.sleep(1)

# update users role
async def roleUpdate():
	pass

# test command
@client.command()
async def test(ctx):
	await ctx.send("Hello, this is a test!")
	userID = ctx.message.author.id
	userName = ctx.message.author.name

# join game command
@client.command()
async def join(ctx):
	userID = ctx.message.author.id
	userName = ctx.message.author.name

	player_exist = database.select_player_exists(userID)

	if (len(player_exist)) == 0:
		player_data = (userID, 1, "town", True)
		database.add_player(player_data)
		inventory_data = (userID, 100, 100, 100, 100, 100, 100, 100, 100)
		database.add_inventory(inventory_data)

		new_player = player.playerClass(database, userID)
		active_player_list.append(new_player)
		api_message = APIMethods.join_game_request(userID, userName)
		await ctx.send(api_message)
	else:
		player_status = database.select_player_status(userID)
		print(player_status)
		if player_status[0] == (0,):
			database.update_player_status(userID, 1)
			api_message = APIMethods.join_game_request(userID, userName)
			new_player = player.playerClass(database, userID)
			active_player_list.append(new_player)
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
	# print(player_status)
	loc = location.lower()
	if player_status[0] == (1,):
		if loc in locationList:
			database.update_player_place(userID, loc)
			#TODO: do thing to get time here
			time = 30
			api_message = APIMethods.move_to_request(userID, loc, time)
			await ctx.send(api_message)
		else:
			await ctx.send("Sorry but {0} isn't a valid place".format(location))
	else:
		await ctx.send("You aren't in the game yet, {0}".format(userName))

# buy command
@client.command()
async def buy(ctx, item, amount):
	userID = ctx.message.author.id
	userName = ctx.message.author.name

	(intown,) = database.select_player_intwon(userID)[0]
	for person in active_player_list:
		if person.player_id == userID:
			if intown: # if player is in a town
				didItWork = person.buyItem(item, amount) # this needs to be assigned to a player
				print(didItWork)
				if didItWork == 0:
					await ctx.send("Trade is unsuccessful partner! {0}".format(userName))
				elif didItWork == 1:
					await ctx.send("Trade successful partner! {0}".format(userName))
				else:
					await ctx.send("That was an invalid input {0}!".format(userName))
		else:
			await ctx.send("You are not in the game! {0}".format(userName))

@client.command()
async def sell(ctx, item, amount):
	userID = ctx.message.author.id
	userName = ctx.message.author.name

	(intown,) = database.select_player_intwon(userID)[0]
	for person in active_player_list:
		if person.player_id == userID:
			if intown: # if player is in a town
				didItWork = person.sellItem(item, amount) # this needs to be assigned to a player
				if didItWork == 1:
					await ctx.send("Trade is unsuccessful partner! {0}".format(userName))
				elif didItWork == 0:
					await ctx.send("Trade successful partner! {0}".format(userName))
				else:
					await ctx.senf("That was an invalid input {0}!".format(userName))
			else:
				await ctx.send("You're not in a town partner! {0}".format(userName))
			break
		# else:
			# await ctx.send("You are not in the game! {0}".format(userName))

@client.command()
async def getInven(ctx):
	user_id = ctx.message.author.id
	user_name = ctx.message.author.name
	player_exist = database.select_player_exists(user_id)
	if len(player_exist) == 0:
		await ctx.send("You need to join the first!")
	else:
		value = random.randint(0, 1000)
		(_, health, gold, gun, booze, hat, horse, lasso, pickaxe) = database.select_user_inventory(user_id)[0]
		message = ("--- Inventory for: {0} ---\n"
				   "- Health: {1}\n"
				   "- Gold: {2}\n"
				   "- Hats: {3}\n" 
				   "- Booze: {4}\n"
				   "- Guns: {5}\n"
				   "- Horses: {6}\n"
				   "- Lassos: {7}\n"
				   "- Pickaxes: {8}\n"
				   "- Brain Cells: {9}").format(user_name, health, gold, hat, booze, gun, horse, lasso, pickaxe, value)
		await ctx.send(message)


@client.event
async def on_message(message):
	if message.author.bot:
		return

	await client.process_commands(message)

file = open("token.txt", "r")
token = str(file.read())
file.close()
client.run(token)