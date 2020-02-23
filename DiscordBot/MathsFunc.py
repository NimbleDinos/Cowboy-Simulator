import math


def calculateLevel(playerXP):
	if playerXP < 105:
		playerLevel = 0
	else:
		playerLevel = math.sqrt((playerXP / 5) - 20)
	return playerLevel


def logistic_func(player_skill):
	return 0.9 / (1 + 8 * math.exp(-0.1 * player_skill))


def time_to(default_time, player_level):
	if player_level >= 100:
		return 0.4 * default_time
	else:
		return default_time * (1 - 0.006 * player_level)