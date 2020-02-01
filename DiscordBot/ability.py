def abilityTest():
	print("abilityTest")

class abilityClass():
	level = 1
	XP = 0
	XPGoal = 100

	def updateXP():
		XP += 10
		if XP > XPGoal:
			updateXPGoal()

	def updateXPGoal():
		XPGoal = XPGoal * 1.1
		XP = 0
		level += 1