def abilityTest():
	print("abilityTest")

<<<<<<< Updated upstream
class abilityClass():
=======
class AbilityClass:
>>>>>>> Stashed changes
	level = 1
	XP = 0
	XPGoal = 100

	def updateXP():
		XP += 10
		if XP > XPGoal:
			updateXPGoal()

<<<<<<< Updated upstream
	def updateXPGoal():
		XPGoal = XPGoal * 1.1
		XP = 0
		level += 1
=======
	def updateXPGoal(self):
		self.XPGoal = self.XPGoal * 1.1
		self.XP = 0
		self.level += 1
>>>>>>> Stashed changes
