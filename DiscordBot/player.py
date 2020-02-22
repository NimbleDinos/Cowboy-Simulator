# Other File Imports
import logisticFunc
import random

item_dict = {
	"gun": 30,
	"booze": 2,
	"hat": 5,
	"horse": 40,
	"lasso": 4,
	"pickaxe": 8
}


class PlayerClass:
	def __init__(self, database, player_id):
		self.database = database
		self.player_id = player_id

	def update_exp(self, skill):
		def exp_formula(x):
			return 0.0017 * x

		(curr_skill,) = self.database.select_player_skill(self.player_id, skill)[0]
		self.database.update_player_skill(skill, exp_formula(curr_skill), self.player_id)

	def panAction(self):
		chanceToFindGold = 0.1  # Don't replace this one
		randomNumber = random.uniform(0, 1)
		if chanceToFindGold > randomNumber:
			(curr_gold,) = self.database.select_player_item("gold", self.player_id)[0]
			self.database.update_player_item("gold", curr_gold + 1, self.player_id)

		# random generator to pick ability to level up
		randomAbility = random.randint(0, 4)
		if randomAbility == 0:
			self.update_exp('shooting')
		if randomAbility == 1:
			self.update_exp('hattitude')
		if randomAbility == 2:
			self.update_exp('riding')
		if randomAbility == 3:
			self.update_exp('catching')
		if randomAbility == 4:
			self.update_exp('mining')

	def action(self, item_count, exp):
		if item_count > 0:
			random_number = random.uniform(0, 1)
			if exp * 0.0017 > random_number:
				return 1
			else:
				return 0

	def mineAction(self):
		(pickaxe_count,) = self.database.select_player_item("pickaxe", self.player_id)[0]
		(mining_exp,) = self.database.select_player_skill(self.player_id, 'mining')
		if self.action(pickaxe_count, logisticFunc.logistic_func(mining_exp * 0.0017)) == 1:
			(curr_gold,) = self.database.select_player_item("gold", self.player_id)[0]
			self.database.update_player_item("gold", curr_gold + 1, self.player_id)
		self.database.update_player_item("pickaxe",  pickaxe_count - 1, self.player_id)
		self.update_exp('mining')


	def shootingAction(self):
		(gun_count,) = self.database.select_player_item("gun", self.player_id)[0]
		(health,) = self.database.select_player_item("health", self.player_id)[0]
		if gun_count > 0 and health > 1:
			self.database.update_player_item("gun", gun_count - 1, self.player_id)
			self.update_exp('shooting')

			(shooting_exp,) = self.database.select_player_skill(self.player_id, 'shooting')[0]
			chanceToBeShot = logisticFunc.logistic_func(shooting_exp * 0.0017)
			randomNumber = random.uniform(0, 1)
			if chanceToBeShot < randomNumber:
				self.database.update_player_item("health", health - 1, self.player_id)

	def ridingAction(self):
		(horse_count,) = self.database.select_player_item("horse", self.player_id)[0]
		if horse_count > 0:
			self.database.update_player_item("horse", horse_count - 1, self.player_id)
			self.update_exp('riding')

	def healAction(self):
		(health,) = self.database.select_player_item("health", self.player_id)[0]
		(booze_count) = self.database.select_player_item("booze", self.player_id)[0]
		if health < 100 and booze_count > 0:
			new_health = health + 4 if health + 4 < 100 else 100
			self.database.update_player_item("health", new_health, self.player_id)
			self.database.update_player_item("booze", booze_count - 1, self.player_id)

	def hatAction(self):
		(hats,) = self.database.select_player_item("hat", self.player_id)[0]
		if hats > 0:
			self.database.update_player_item("hat", hats - 1, self.player_id)
			self.update_exp('hattitude')

	def catchAction(self):
		(lasso_count,) = self.database.select_player_item("lasso", self.player_id)[0]
		(catch_exp,) = self.database.select_player_skill(self.player_id, 'catching')[0]
		if self.action(lasso_count, logisticFunc.logistic_func(catch_exp * 0.0017)) == 1:
			(horse_count,) = self.database.select_player_item("horse", self.player_id)[0]
			self.database.update_player_item("horse", horse_count + 1, self.player_id)
		self.database.update_player_item("lasso", lasso_count - 1, self.player_id)
		self.update_exp('catching')

	def __buy_item(self, item, int_amount):
		(current_gold,) = self.database.select_player_item("gold", self.player_id)[0]
		cost = item_dict.get(item) * int_amount
		print(current_gold)

		if current_gold - cost < 0:
			return 1
		else:
			self.database.update_player_item("gold", current_gold - cost, self.player_id)
			(item_count,) = self.database.select_player_item(item, self.player_id)[0]
			self.database.update_player_item(item, item_count + int_amount, self.player_id)
			return 0

	# buy item
	def buyItem(self, item, amount):
		try:
			lower_item = item.lower()
			int_amount = int(amount)

			if lower_item not in item_dict:
				return 4

			return self.__buy_item(lower_item, int_amount)
		except ValueError:
			return 3

	def __sell_item(self, item, int_amount):
		(current_gold,) = self.database.select_player_item("gold", self.player_id)[0]
		sell_total = item_dict.get(item) * int_amount

		(item_count,) = self.database.select_player_item(item, self.player_id)[0]
		if item_count < int_amount:
			return 1
		else:
			self.database.update_player_item("gold", current_gold + sell_total, self.player_id)
			self.database.update_player_item(item, item_count - int_amount, self.player_id)
			return 0

	# sell item
	def sellItem(self, item, amount):
		try:
			int_amount = int(amount)
			lower_item = item.lower()

			if lower_item not in item_dict:
				return 4

			return self.__sell_item(lower_item, int_amount)
		except ValueError:
			return 3
