# Other File Imports
import logisticFunc
import ability
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

	# abilities
	Shooting = ability.AbilityClass()
	Hattitude = ability.AbilityClass()
	Riding = ability.AbilityClass()
	Catching = ability.AbilityClass()
	Mining = ability.AbilityClass()

	def panAction(self):
		chanceToFindGold = 0.1  # Don't replace this one
		randomNumber = random.uniform(0, 1)
		if chanceToFindGold > randomNumber:
			(curr_gold,) = self.database.select_user_item("gold", self.player_id)[0]
			self.database.update_player_item("gold", curr_gold + 1, self.player_id)

		# random generator to pick ability to level up
		randomAbility = random.randint(0, 4)
		if randomAbility == 0:
			self.Shooting.updateXP()
		if randomAbility == 1:
			self.Hattitude.updateXP()
		if randomAbility == 2:
			self.Riding.updateXP()
		if randomAbility == 3:
			self.Catching.updateXP()
		if randomAbility == 4:
			self.Mining.updateXP()

	def action(self, item_count, chance):
		if item_count > 0:
			random_number = random.uniform(0, 1)
			if chance > random_number:
				return 1
			else:
				return 0

	def mineAction(self):
		(pickaxe_count,) = self.database.select_user_item("pickaxe", self.player_id)[0]
		if self.action(pickaxe_count, logisticFunc.logistic_func(self.Mining.level)) == 1:
			(curr_gold,) = self.database.select_user_item("gold", self.player_id)[0]
			self.database.update_player_item("gold", curr_gold + 1, self.player_id)
		self.database.update_player_item("pickaxe",  pickaxe_count - 1, self.player_id)
		self.Mining.updateXP()

	def ridingAction(self):
		(horse_count,) = self.database.select_user_item("horse", self.player_id)[0]
		if horse_count > 0:
			self.database.update_player_item("horse", horse_count - 1, self.player_id)
			self.Riding.updateXP()

	def shootingAction(self):
		(gun_count,) = self.database.select_user_item("gun", self.player_id)[0]
		(health,) = self.database.select_user_item("health", self.player_id)[0]
		if gun_count > 0 and health > 1:
			self.database.update_player_item("gun", gun_count - 1, self.player_id)
			self.Shooting.updateXP()

			chanceToBeShot = logisticFunc.logistic_func(self.Shooting.level)
			randomNumber = random.uniform(0, 1)
			if chanceToBeShot < randomNumber:
				self.database.update_player_item("health", health - 1, self.player_id)

	def healAction(self):
		(health,) = self.database.select_user_item("health", self.player_id)[0]
		(booze_count) = self.database.select_user_item("booze", self.player_id)[0]
		if health < 100 and booze_count > 0:
			new_health = health + 4 if health + 4 < 100 else 100
			self.database.update_player_item("health", new_health, self.player_id)
			self.database.update_player_item("booze", booze_count - 1, self.player_id)

	def hatAction(self):
		(hats,) = self.database.select_user_item("hat", self.player_id)[0]
		if hats > 0:
			self.database.update_player_item("hat", hats - 1, self.player_id)
			self.Hattitude.updateXP()

	def catchAction(self):
		(lasso_count,) = self.database.select_user_item("lasso", self.player_id)[0]
		if self.action(lasso_count, logisticFunc.logistic_func(self.Catching.level)) == 1:
			(horse_count,) = self.database.select_user_item("horse", self.player_id)[0]
			self.database.update_player_item("horse", horse_count + 1, self.player_id)
		self.database.update_player_item("lasso", lasso_count - 1, self.player_id)
		self.Catching.updateXP()

	def _buy_item(self, item, int_amount):
		(current_gold,) = self.database.select_user_item("gold", self.player_id)[0]
		cost = item_dict.get(item) * int_amount
		print(current_gold)

		if current_gold - cost < 0:
			return 1
		else:
			self.database.update_player_item("gold", current_gold - cost, self.player_id)
			(item_count,) = self.database.select_user_item(item, self.player_id)[0]
			self.database.update_player_item(item, item_count + int_amount, self.player_id)
			return 0

	# buy item
	def buyItem(self, item, amount):
		try:
			lower_item = item.lower()
			int_amount = int(amount)

			if lower_item not in item_dict:
				return 4

			return self._buy_item(lower_item, int_amount)
		except ValueError:
			return 3

	def _sell_item(self, item, int_amount):
		(current_gold,) = self.database.select_user_item("gold", self.player_id)[0]
		sell_total = item_dict.get(item) * int_amount

		(item_count,) = self.database.select_user_item(item, self.player_id)[0]
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

			return self._sell_item(lower_item, int_amount)
		except ValueError:
			return 3
