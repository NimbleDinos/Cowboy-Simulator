def abilityTest():
	print("abilityTest")

class AbilityClass:
	level = 1
	XP = 0
	XPGoal = 100

	def updateXP(self):
		self.XP += 10
		if self.XP > self.XPGoal:
			self.updateXPGoal()
 
	def updateXPGoal(self):
		self.XPGoal = self.XPGoal * 1.1
		self.XP = 0
		self.level += 1