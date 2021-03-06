import datetime
import asyncio

# Discord Imports
import discord
import discord.ext
from discord.ext.commands import Bot
from discord.ext import commands
import math

# Other Files Imports
import player
import APIMethods

import db
import random
import leaderboard
import MathsFunc

import pandas as pd

locationList = ["hull", "lincoln", "sheffield", "corral", "gold-mine", "plains", "river", "shooting-range",
                "travelling"]

bot_prefix = "!"
client = commands.Bot(command_prefix=bot_prefix)
client.remove_command("help")

# global variables
active_player_list = []

database_loc = r"./db/database.sql"
database = db.database.Database(database_loc)
database.create_player_table()
database.create_inventory_table()
database.create_skills_table()
database.update_all_player_status()

leaderboard = leaderboard.Leaderboard(database)

index = ["shooting-range", "hull", "sheffield", "corral", "mines", "plains", "river", "lincoln"]
times_df = pd.read_csv("times.csv", index_col=['place'])


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
		# print(active_player_list)
		leaderboard.get_leaderboard()
		for person in active_player_list:
			(loc,) = database.select_player_place(person.player_id)[0]
			# test = database.select_user_gold(person.player_id)
			print("GOLD {0}".format(test))
			# do thing based on location
			if loc == "travelling":
				database.update_player_intown(person.player_id, False)
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

	def add_player():
		database.update_player_status(userID, 1)
		new_player = player.PlayerClass(database, userID)
		active_player_list.append(new_player)
		api_message = APIMethods.join_game_request(userID, userName)
		return api_message

	if (len(player_exist)) == 0:
		player_data = (userID, userName, 1, "lincoln", True)
		database.add_player(player_data)
		inventory_data = (userID, 100, 10, 0, 0, 0, 0, 0, 0)
		database.add_inventory(inventory_data)
		skill_data = (userID, 0, 0, 0, 0, 0)
		database.add_skills(skill_data)

		message = add_player()
		await ctx.send(message)
	else:
		player_status = database.select_player_status(userID)
		if player_status[0] == (0,):
			message = add_player()
			await ctx.send(message)
		else:
			await ctx.send("You are already in the game " + userName + "!")


@client.command()
async def leave(ctx):
	user_id = ctx.message.author.id
	user_name = ctx.message.author.name

	player_exist = database.select_player_exists(user_id)
	if (len(player_exist)) == 0:
		await ctx.send("You are not currently in the game " + user_name + "!")
	else:
		player_status = database.select_player_status(user_id)
		if player_status[0] == (0,):
			await ctx.send("You are not currently in the game " + user_name + "!")
		else:
			database.update_player_status(user_id, 0)
			APIMethods.join_game_request(user_id, user_name)
			for person in active_player_list:
				if person.player_id == user_id:
					active_player_list.remove(person)
					break
			await ctx.send("See you soon " + user_name + "!")


# go to command
@client.command()
async def goto(ctx, location):
	userID = ctx.message.author.id
	userName = ctx.message.author.name

	# print(player_status)
	loc = location.lower()
	if loc in locationList:
		player_status = database.select_player_status(userID)
		if player_status[0] == (1,):
			(curr_player_loc,) = database.select_player_place(userID)[0]
			if loc == curr_player_loc:
				await ctx.send("You are already in {0} {1}".format(loc, userName))
			elif curr_player_loc == "travelling":
				await ctx.send("You are already travelling somewhere {0}!".format(userName))
			else:
				print(curr_player_loc)
				print(loc)
				default_time = times_df.lookup([curr_player_loc], [loc])[0]
				(riding_exp,) = database.select_player_skill(userID, 'riding')[0]
				travel_time = int(round(MathsFunc.time_to(default_time, MathsFunc.calculateLevel(riding_exp))))

				api_message, status_code = APIMethods.move_to_request(userID, loc, travel_time)
				await ctx.send(api_message)
				if status_code == 200:
					database.update_player_place(userID, "travelling")
					print(travel_time)
					await update_loc(userID, loc, travel_time)
					await ctx.send("{0} has arrived in {1}!".format(userName, loc))
		else:
			await ctx.send("You aren't in the game yet, {0}".format(userName))
	else:
		await ctx.send("Sorry but {0} isn't a valid place".format(location))


async def update_loc(player_id, loc, time):
	await asyncio.sleep(time)
	database.update_player_place(player_id, loc)


# buy command
@client.command()
async def buy(ctx, item, amount):
	userID = ctx.message.author.id
	userName = ctx.message.author.name

	for person in active_player_list:
		if person.player_id == userID:
			(intown,) = database.select_player_intown(userID)[0]
			if intown:  # if player is in a town
				(place,) = database.select_player_place(userID)[0]
				didItWork = person.buy_item(item, amount, place)
				print(didItWork)
				if didItWork == 1:
					await ctx.send("Trade is unsuccessful partner! {0}".format(userName))
				elif didItWork == 0:
					await ctx.send("Trade successful partner! {0}".format(userName))
				else:
					await ctx.send("That was an invalid input {0}!".format(userName))
			else:
				await ctx.send("You must be in a town to trade {0}!".format(userName))
			break
		else:
			await ctx.send("You are not in the game! {0}".format(userName))


@client.command()
async def sell(ctx, item, amount):
	userID = ctx.message.author.id
	userName = ctx.message.author.name

	for person in active_player_list:
		if person.player_id == userID:
			(intown,) = database.select_player_intown(userID)[0]
			if intown:  # if player is in a town
				(place,) = database.select_player_place(userID)[0]
				didItWork = person.sell_item(item, amount, place)  # this needs to be assigned to a player
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
		(_, health, gold, gun, booze, hat, horse, lasso, pickaxe) = database.select_player_inventory(user_id)[0]
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


@client.command()
async def getSkills(ctx):
	user_id = ctx.message.author.id
	user_name = ctx.message.author.name
	player_exist = database.select_player_exists(user_id)
	if len(player_exist) == 0:
		await ctx.send("You need to join first!")
	else:
		value = random.randint(0, 100)
		(_, hattitude, shooting, riding, catching, mining) = database.select_player_skills(user_id)[0]
		message = ("--- Levels for: {0} ---\n"
		           "- Hattitude: {1}\n"
		           "- Shooting: {2}\n"
		           "- Riding: {3}\n"
		           "- Catching: {4}\n"
		           "- Mining: {5}\n"
		           "- Soberness: {6}%").format(user_name, math.floor(MathsFunc.calculateLevel(hattitude)),
		                                       math.floor(MathsFunc.calculateLevel(shooting)),
		                                       math.floor(MathsFunc.calculateLevel(riding)),
		                                       math.floor(MathsFunc.calculateLevel(catching)),
		                                       math.floor(MathsFunc.calculateLevel(mining)),
		                                       value)
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
