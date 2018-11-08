# Defines all neccessary characteristics of a champion
class Champion:
	
	def __init__(self,champ_name,win_ratio,games_played,kda_ratio):
		self.champ_name = champ_name
		self.win_ratio = win_ratio
		self.games_played = games_played
		self.kda_ratio = kda_ratio

	# prints champ data (developer purposes)
	def print_champ_data(self):
		print(self.champ_name + ", " + str(self.win_ratio) + ", " + str(self.games_played) + ", " + str(self.kda_ratio))
	
	def get_name(self):
		return self.champ_name

	def get_winrate(self):
		return self.win_ratio

	def get_games_played(self):
		return self.games_played

	def get_kda(self):
		return self.kda_ratio