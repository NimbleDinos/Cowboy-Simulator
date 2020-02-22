import math


def calculateLevel(playerXP):
	if playerXP < 105:
		playerLevel = 0
	else:
		playerLevel = math.sqrt((playerXP / 5) - 20)
	return playerLevel


def logistic_func(player_skill):
	return 0.9 / (1 + 8 * math.exp(-0.1 * player_skill))
