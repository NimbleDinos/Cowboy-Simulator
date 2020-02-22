
class Leaderboard:

	multipliers = [1.5, 1.25, 1, 0.9, 0.75]

	def __init__(self, database):
		self.database = database

	def get_leaderboard(self):
		player_skills = self.database.select_all_skills()
		player_scores = []
		for row in player_skills:
			print("got row")
			score = 0.0
			for col in range(len(row)):
				if col == 0:
					continue
				score = score + self.multipliers[col - 1] * row[col]
			player_scores.append((row[0], round(score*10)))
		desc_lb = sorted(player_scores, key=lambda x: x[1], reverse=True)
		print(desc_lb)
		return desc_lb
